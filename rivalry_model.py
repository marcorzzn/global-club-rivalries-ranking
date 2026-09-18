import pandas as pd
import numpy as np
import datetime

# --- CONFIGURAZIONE PESI MODELLO ---
# Modifica questi valori per fare tuning dell'Indice di Rivalità
DEFAULT_WEIGHTS = {
    'w_c': 0.35,  # Competitività: motore principale, penalizza i domini assoluti.
    'w_p': 0.25,  # Posta in Palio: densità di scontro ai vertici.
    'w_l': 0.20,  # Longevità: storicità e volume di scontri nel tempo.
    'w_t': 0.20   # Prestigio: peso specifico globale delle due società (trofei).
}

# Moltiplicatore applicato in caso di stracittadina (Derby)
DERBY_BONUS = 1.15
# -----------------------------------

class RivalryIndexCalculator:
    def __init__(self, w_c=DEFAULT_WEIGHTS['w_c'], w_p=DEFAULT_WEIGHTS['w_p'], w_l=DEFAULT_WEIGHTS['w_l'], w_t=DEFAULT_WEIGHTS['w_t']):
        """
        Inizializza il calcolatore con i pesi dei 4 parametri.
        La somma dei pesi dovrebbe essere 1.
        """
        self.set_weights(w_c, w_p, w_l, w_t)

    def set_weights(self, w_c, w_p, w_l, w_t):
        """Permette di variare liberamente i pesi dei 4 parametri."""
        total = w_c + w_p + w_l + w_t
        if total == 0:
            raise ValueError("La somma dei pesi non può essere zero.")
        
        self.w_c = w_c / total
        self.w_p = w_p / total
        self.w_l = w_l / total
        self.w_t = w_t / total

    def compute_rivalry_index(self, matches_history, teams_metadata):
        """
        Calcola l'Indice di Rivalità R per ogni coppia di squadre (A, B) 
        che si sono affrontate almeno 10 volte.
        """
        matches = matches_history.copy()
        
        # Identifichiamo team 1 e team 2 in ordine alfabetico
        matches['team_1'] = np.where(matches['team_a'] < matches['team_b'], matches['team_a'], matches['team_b'])
        matches['team_2'] = np.where(matches['team_a'] < matches['team_b'], matches['team_b'], matches['team_a'])
        
        matches['goals_1'] = np.where(matches['team_a'] < matches['team_b'], matches['goals_a'], matches['goals_b'])
        matches['goals_2'] = np.where(matches['team_a'] < matches['team_b'], matches['goals_b'], matches['goals_a'])
        
        matches['win_1'] = (matches['goals_1'] > matches['goals_2']).astype(int)
        matches['win_2'] = (matches['goals_2'] > matches['goals_1']).astype(int)
        
        matches['goal_diff_abs'] = abs(matches['goals_1'] - matches['goals_2'])

        # Raggruppamento
        pairs = matches.groupby(['team_1', 'team_2']).agg(
            total_matches=('match_id', 'count'),
            wins_1=('win_1', 'sum'),
            wins_2=('win_2', 'sum'),
            avg_goal_diff=('goal_diff_abs', 'mean')
        ).reset_index()

        pairs = pairs[pairs['total_matches'] >= 10].copy()
        if pairs.empty:
            return pd.DataFrame()

        # 1. Competitività (C)
        win_diff_ratio = abs(pairs['wins_1'] - pairs['wins_2']) / pairs['total_matches']
        goal_diff_penalty = np.maximum(0, (pairs['avg_goal_diff'] - 1.5) * 0.1)
        pairs['C'] = np.clip(1 - win_diff_ratio - goal_diff_penalty, 0, 1)

        # 2. Longevità (L)
        max_matches = pairs['total_matches'].max()
        if max_matches > 1:
            pairs['L'] = np.log(pairs['total_matches']) / np.log(max_matches)
        else:
            pairs['L'] = 0

        # Merge Metadati
        team_meta = teams_metadata.set_index('team_name')
        
        pairs = pairs.join(team_meta[['city', 'total_major_trophies', 'season_final_standing']], on='team_1')
        pairs = pairs.rename(columns={'city': 'city_1', 'total_major_trophies': 'trophies_1', 'season_final_standing': 'standings_1'})
        
        pairs = pairs.join(team_meta[['city', 'total_major_trophies', 'season_final_standing']], on='team_2')
        pairs = pairs.rename(columns={'city': 'city_2', 'total_major_trophies': 'trophies_2', 'season_final_standing': 'standings_2'})

        # Gestione NaN su trofei
        pairs['trophies_1'] = pairs['trophies_1'].fillna(0)
        pairs['trophies_2'] = pairs['trophies_2'].fillna(0)

        # 4. Prestigio / Pressione (T)
        pairs['total_trophies_pair'] = pairs['trophies_1'] + pairs['trophies_2']
        max_trophies_pair = pairs['total_trophies_pair'].max()
        if max_trophies_pair > 0:
            pairs['T'] = pairs['total_trophies_pair'] / max_trophies_pair
        else:
            pairs['T'] = 0

        # 5. Bonus Derby Geografico (D)
        pairs['D'] = np.where(pairs['city_1'] == pairs['city_2'], DERBY_BONUS, 1.0)

        # 2. Posta in Palio e Gerarchia (P)
        def compute_hierarchy(row):
            st1 = row['standings_1'] if isinstance(row['standings_1'], dict) else {}
            st2 = row['standings_2'] if isinstance(row['standings_2'], dict) else {}
            common_seasons = set(st1.keys()).intersection(set(st2.keys()))
            if not common_seasons:
                return 0.0
            
            diffs = [abs(st1[s] - st2[s]) for s in common_seasons]
            mean_diff = np.mean(diffs)
            
            return 1.0 / (1.0 + (mean_diff / 2.0))

        pairs['P'] = pairs.apply(compute_hierarchy, axis=1)

        # Calcolo finale dell'Indice R
        pairs['R_base'] = (
            self.w_c * pairs['C'] +
            self.w_p * pairs['P'] +
            self.w_l * pairs['L'] +
            self.w_t * pairs['T']
        )
        
        pairs['R_final'] = pairs['R_base'] * pairs['D']
        
        return pairs.sort_values(by='R_final', ascending=False).reset_index(drop=True)

if __name__ == "__main__":
    print(f"Calcolatore inizializzato con pesi: C={DEFAULT_WEIGHTS['w_c']}, P={DEFAULT_WEIGHTS['w_p']}, L={DEFAULT_WEIGHTS['w_l']}, T={DEFAULT_WEIGHTS['w_t']}")
    
    # --- Codice di Esempio / Esecuzione ---
    # In un caso reale, qui caricheresti i csv generati dall'ETL:
    import os
    if os.path.exists("matches_history.csv") and os.path.exists("teams_metadata.csv"):
        import json
        
        matches_df = pd.read_csv("matches_history.csv")
        teams_df = pd.read_csv("teams_metadata.csv")
        
        # Deserializziamo il json dei piazzamenti se necessario
        teams_df['season_final_standing'] = teams_df['season_final_standing'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
        
        calc = RivalryIndexCalculator()
        results = calc.compute_rivalry_index(matches_df, teams_df)
        
        print("\nCalcolo Completato. Esportazione in 'top_rivalries.csv'...")
        results.to_csv("top_rivalries.csv", index=False)
        print(results[['team_1', 'team_2', 'R_final']].head(20))
    else:
        print("I file CSV di base non esistono. Esegui prima ETL e Scraper!")
