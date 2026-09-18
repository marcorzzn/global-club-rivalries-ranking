import pandas as pd
import requests
import io
import time
import json
import os

class OpenDataFootballETL:
    def __init__(self):
        """
        Estrattore basato su fonti Open Data pubbliche (es. football-data.co.uk).
        Non richiede alcuna API Key, né registrazioni, ed è velocissimo.
        Supporta i Top 5 campionati europei.
        """
        # Mappatura leghe supportate dal portale
        self.leagues_map = {
            'Serie_A': 'I1',
            'Premier_League': 'E0',
            'La_Liga': 'SP1',
            'Bundesliga': 'D1',
            'Ligue_1': 'F1'
        }
        
    def generate_season_code(self, year_start):
        """Genera il codice stagione (es. 2021 -> '2122')."""
        y1 = str(year_start)[-2:]
        y2 = str(year_start + 1)[-2:]
        return f"{y1}{y2}"
        
    def fetch_matches_from_csv(self, league_name, year_start):
        """
        Scarica il CSV pubblico della singola stagione.
        """
        season_code = self.generate_season_code(year_start)
        league_code = self.leagues_map.get(league_name)
        
        if not league_code:
            raise ValueError(f"Lega {league_name} non supportata.")
            
        url = f"https://www.football-data.co.uk/mmz4281/{season_code}/{league_code}.csv"
        
        try:
            # Il portale potrebbe bloccare richieste senza User-Agent
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                print(f"  [!] Dati non disponibili per {league_name} stagione {year_start}/{year_start+1}")
                return pd.DataFrame()
                
            df = pd.read_csv(io.StringIO(response.text), on_bad_lines='skip')
            
            # Filtra le colonne che ci interessano e rinomina per farle combaciare col modello
            # FTHG = Full Time Home Goals, FTAG = Full Time Away Goals
            essential_cols = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']
            
            if not all(col in df.columns for col in essential_cols):
                print(f"  [!] Colonne mancanti nel CSV di {season_code}")
                return pd.DataFrame()
                
            df = df[essential_cols].copy()
            df = df.dropna(subset=['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG'])
            
            df = df.rename(columns={
                'Date': 'date',
                'HomeTeam': 'team_a',
                'AwayTeam': 'team_b',
                'FTHG': 'goals_a',
                'FTAG': 'goals_b'
            })
            
            # Formattazioni
            df['match_id'] = [f"{season_code}_{league_code}_{i}" for i in range(len(df))]
            df['competition'] = league_name
            df['season'] = f"{year_start}/{year_start+1}"
            df['goals_a'] = df['goals_a'].astype(int)
            df['goals_b'] = df['goals_b'].astype(int)
            
            # Per evitare problemi con formati data multipli (dd/mm/yy vs dd/mm/yyyy)
            df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
            
            return df
            
        except Exception as e:
            print(f"  [!] Errore download {url}: {e}")
            return pd.DataFrame()

    def compute_standings(self, df_matches):
        """
        Calcola dinamicamente la classifica finale dell'anno basandosi sui risultati delle partite.
        In questo modo non abbiamo bisogno di scaricare le classifiche da API esterne!
        """
        standings = {}
        
        # Inizializza a zero
        all_teams = set(df_matches['team_a']).union(set(df_matches['team_b']))
        for t in all_teams:
            standings[t] = 0
            
        for _, row in df_matches.iterrows():
            if row['goals_a'] > row['goals_b']:
                standings[row['team_a']] += 3
            elif row['goals_a'] < row['goals_b']:
                standings[row['team_b']] += 3
            else:
                standings[row['team_a']] += 1
                standings[row['team_b']] += 1
                
        # Ordina per punti e genera il rank (1, 2, 3...)
        sorted_teams = sorted(standings.items(), key=lambda x: x[1], reverse=True)
        ranks = {team: rank for rank, (team, points) in enumerate(sorted_teams, start=1)}
        
        return ranks

    def build_dataset(self, league_name, start_year, end_year):
        print(f"--- Estrazione dati Open Source per {league_name} ({start_year}-{end_year}) ---")
        
        all_matches = []
        teams_data = {}
        
        for year in range(start_year, end_year):
            print(f"Scaricamento stagione {year}/{year+1}...")
            df_season = self.fetch_matches_from_csv(league_name, year)
            
            if df_season.empty:
                continue
                
            all_matches.append(df_season)
            
            # Calcolo automatico della classifica!
            ranks = self.compute_standings(df_season)
            season_str = f"{year}/{year+1}"
            
            for team, rank in ranks.items():
                if team not in teams_data:
                    # Inizializziamo senza città (per le città useremo wikidata o db fisso dopo)
                    teams_data[team] = {'season_final_standing': {}}
                teams_data[team]['season_final_standing'][season_str] = rank
                
            time.sleep(1) # Cortesia verso il server open source
            
        if not all_matches:
            print("Nessun dato recuperato.")
            return pd.DataFrame(), pd.DataFrame()
            
        final_matches_df = pd.concat(all_matches, ignore_index=True)
        
        # Costruzione del dataframe metadata
        teams_list = []
        for team, data in teams_data.items():
            teams_list.append({
                'team_name': team,
                'league': league_name,
                'city': 'Unknown', # Da sistemare in una run successiva
                'total_major_trophies': 0,
                'season_final_standing': data['season_final_standing']
            })
            
        final_teams_df = pd.DataFrame(teams_list)
        return final_matches_df, final_teams_df

if __name__ == "__main__":
    etl = OpenDataFootballETL()
    
    # Esempio: Scarichiamo Serie A dal 2005 al 2023 
    # (football-data.co.uk ha dati fin dagli anni 90 per i top campionati!)
    LEAGUE = 'Serie_A'
    START_YEAR = 2005
    END_YEAR = 2023
    
    df_matches, df_teams = etl.build_dataset(LEAGUE, START_YEAR, END_YEAR)
    
    if not df_matches.empty:
        # Serializzazione della classifica
        df_teams['season_final_standing'] = df_teams['season_final_standing'].apply(json.dumps)
        
        # Salvataggio
        df_matches.to_csv("matches_history.csv", index=False)
        df_teams.to_csv("teams_metadata.csv", index=False)
        
        print("\nPipeline Open Source Completata con Successo!")
        print(f"Salvato matches_history.csv ({len(df_matches)} incontri)")
        print(f"Salvato teams_metadata.csv ({len(df_teams)} squadre totali)")
    else:
        print("\nErrore nella generazione dei dati.")
