import requests
import pandas as pd
import time
import json
import os

class APIFootballETL:
    def __init__(self, api_key, checkpoint_file='etl_checkpoint.json'):
        self.api_key = api_key
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-apisports-key": self.api_key
        }
        self.checkpoint_file = checkpoint_file
        self.call_count = 0
        self.load_checkpoint()
        
    def load_checkpoint(self):
        """Carica lo stato per riprendere il lavoro da dove si era interrotto."""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                self.state = json.load(f)
            print(f"Checkpoint caricato: {len(self.state['processed_seasons'])} stagioni già processate.")
        else:
            self.state = {
                'processed_seasons': [], # Lista di stringhe formato "leagueId_year"
                'matches': [], 
                'teams_metadata': {}
            }
            
    def save_checkpoint(self):
        """Salva fisicamente su disco l'avanzamento attuale."""
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.state, f)
        print(f"[*] Checkpoint salvato. Totale chiamate API in questa sessione: {self.call_count}")

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Incrementiamo il contatore e gestiamo il salvataggio automatico ogni 50 chiamate
            self.call_count += 1
            if self.call_count % 50 == 0:
                self.save_checkpoint()
                
            time.sleep(0.5) # Rate limit safety
            return data.get('response', [])
        except requests.exceptions.RequestException as e:
            print(f"Errore API {endpoint}: {e}")
            return []

    def fetch_historical_fixtures(self, league_id, season):
        fixtures = self._make_request("fixtures", params={"league": league_id, "season": season})
        matches_data = []
        for f in fixtures:
            if f['fixture']['status']['short'] not in ['FT', 'AET', 'PEN']:
                continue
            matches_data.append({
                'match_id': str(f['fixture']['id']),
                'date': f['fixture']['date'],
                'team_a': f['teams']['home']['name'],
                'team_b': f['teams']['away']['name'],
                'goals_a': f['goals']['home'],
                'goals_b': f['goals']['away'],
                'competition': f['league']['name'],
                'season': str(season)
            })
        return matches_data

    def fetch_teams_info(self, league_id, season):
        """Estrae le informazioni base delle squadre inclusa la CITTÀ dallo stadio (venue)."""
        teams = self._make_request("teams", params={"league": league_id, "season": season})
        teams_info = {}
        for t in teams:
            team_name = t['team']['name']
            city = t['venue']['city'] if t['venue'] and t['venue']['city'] else 'Unknown'
            teams_info[team_name] = city
        return teams_info

    def fetch_standings(self, league_id, season):
        standings_response = self._make_request("standings", params={"league": league_id, "season": season})
        standings_dict = {}
        if not standings_response:
            return standings_dict
        try:
            league_standings = standings_response[0]['league']['standings'][0]
            for team_rank in league_standings:
                standings_dict[team_rank['team']['name']] = team_rank['rank']
        except (IndexError, KeyError):
            pass
        return standings_dict

    def build_dataset(self, league_id, start_year, end_year):
        for year in range(start_year, end_year + 1):
            season_key = f"{league_id}_{year}"
            
            # Skip se la stagione è già stata scaricata nei run precedenti
            if season_key in self.state['processed_seasons']:
                print(f"Stagione {year} (Lega {league_id}) già processata. Salto.")
                continue
                
            print(f"Elaborazione Stagione {year}...")
            
            # 1. Recupero Teams & Città
            cities_dict = self.fetch_teams_info(league_id, year)
            
            # 2. Recupero Incontri
            season_matches = self.fetch_historical_fixtures(league_id, year)
            self.state['matches'].extend(season_matches)
            
            # 3. Recupero Classifiche
            season_ranks = self.fetch_standings(league_id, year)
            
            # 4. Aggiornamento Teams Metadata State
            for team, rank in season_ranks.items():
                if team not in self.state['teams_metadata']:
                    self.state['teams_metadata'][team] = {
                        'city': cities_dict.get(team, 'Unknown'),
                        'season_final_standing': {}
                    }
                self.state['teams_metadata'][team]['season_final_standing'][str(year)] = rank
                # Aggiorna la città se precedentemente "Unknown"
                if self.state['teams_metadata'][team]['city'] == 'Unknown' and team in cities_dict:
                    self.state['teams_metadata'][team]['city'] = cities_dict[team]
                    
            self.state['processed_seasons'].append(season_key)
            self.save_checkpoint() # Salva progressi a fine di ogni anno completato
            
        return self._generate_dataframes()

    def _generate_dataframes(self):
        # Ricostruzione Matches DataFrame
        if self.state['matches']:
            df_matches = pd.DataFrame(self.state['matches'])
            df_matches['date'] = pd.to_datetime(df_matches['date'])
        else:
            df_matches = pd.DataFrame()
            
        # Ricostruzione Teams DataFrame
        teams_list = []
        for team_name, data in self.state['teams_metadata'].items():
            teams_list.append({
                'team_name': team_name,
                'league': 'N/A', 
                'city': data['city'],
                'total_major_trophies': 0, # Andrà riempito con lo scraper di Trophies
                'season_final_standing': data['season_final_standing']
            })
        df_teams = pd.DataFrame(teams_list)
        return df_matches, df_teams
        
    def merge_with_historical_csv(self, api_matches, pre_2010_csv_path):
        """Fonde i dati API post-2010 con il dump locale pre-2010."""
        if os.path.exists(pre_2010_csv_path):
            print(f"Trovato file storico: {pre_2010_csv_path}. Procedo al merge...")
            df_historical = pd.read_csv(pre_2010_csv_path)
            # Assicuriamoci che i formati coincidano prima del merge
            df_historical['date'] = pd.to_datetime(df_historical['date'])
            merged = pd.concat([df_historical, api_matches], ignore_index=True)
            # Rimuoviamo eventuali duplicati
            merged = merged.drop_duplicates(subset=['match_id'])
            return merged
        else:
            print(f"File storico {pre_2010_csv_path} non trovato. Procedo solo con i dati API.")
            return api_matches

if __name__ == "__main__":
    API_KEY = os.getenv("APIFootball_KEY", "INSERISCI_QUI_LA_TUA_CHIAVE")
    LEAGUE_ID = 135 # Serie A
    
    # Nuovo requisito: API solo per dati moderni
    START_YEAR = 2010
    END_YEAR = 2023
    
    if API_KEY != "INSERISCI_QUI_LA_TUA_CHIAVE":
        etl = APIFootballETL(api_key=API_KEY)
        
        # Esecuzione processo API (riprenderà in automatico se c'è un checkpoint)
        df_api_matches, df_teams = etl.build_dataset(LEAGUE_ID, START_YEAR, END_YEAR)
        
        # Merge con dataset storico pre-2010
        final_matches = etl.merge_with_historical_csv(df_api_matches, "historical_data_pre_2010.csv")
        
        # Export finale
        final_matches.to_csv("matches_history.csv", index=False)
        df_teams['season_final_standing'] = df_teams['season_final_standing'].apply(json.dumps)
        df_teams.to_csv("teams_metadata.csv", index=False)
        print("ETL completato e dataset combinato esportato con successo.")
    else:
        print("Inserisci la tua API Key per avviare.")
