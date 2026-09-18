# Architettura e Calcolo Indice di Rivalità Storica

Questo progetto definisce l'architettura dati e l'algoritmo matematico per calcolare un Indice di Rivalità oggettivo (dal 1976 al 2026) per le squadre delle Top 50 Leghe Opta.

## 1. Struttura del Database (Schema Dati Desiderato)

I dati saranno raccolti e memorizzati in due tabelle principali (rappresentate nei dataframe `matches_history` e `teams_metadata` dello script):

### `matches_history`
Contiene lo storico di tutti gli incontri ufficiali disputati, garantendo un'oggettività al 100% (solo risultati verificabili e inequivocabili).

| Colonna       | Tipo Dati | Descrizione                                                                 |
|---------------|-----------|-----------------------------------------------------------------------------|
| `match_id`    | String    | Identificativo univoco della partita.                                       |
| `date`        | Date/Time | Data in cui si è disputato l'incontro.                                      |
| `team_a`      | String    | Nome o ID univoco della squadra in casa (o sorteggiata come tale).          |
| `team_b`      | String    | Nome o ID univoco della squadra in trasferta.                               |
| `goals_a`     | Integer   | Reti segnate dalla `team_a`.                                                |
| `goals_b`     | Integer   | Reti segnate dalla `team_b`.                                                |
| `competition` | String    | Nome della competizione (es. Serie A, Champions League).                    |
| `season`      | String    | Stagione sportiva (es. '2023/2024').                                        |

### `teams_metadata`
Contiene le informazioni aggregate per squadra, utili al calcolo del prestigio e delle penalità di gerarchia/derby.

| Colonna                 | Tipo Dati   | Descrizione                                                                 |
|-------------------------|-------------|-----------------------------------------------------------------------------|
| `team_name`             | String      | Nome o ID univoco della squadra.                                            |
| `league`                | String      | Lega Opta di appartenenza o lega principale.                                |
| `city`                  | String      | Città di riferimento (per individuare i derby tramite `city_A == city_B`).  |
| `total_major_trophies`  | Integer     | Somma dei titoli di lega principali e coppe internazionali vinte.           |
| `season_final_standing` | JSON/Dict   | Dizionario Chiave-Valore (Stagione -> Posizione in Classifica).             |

---

## 2. API Consigliate per il Recupero Dati Storici (1976-2026)

Per popolare questo database in modo affidabile e automatico, l'uso di un servizio come **API-Football** (disponibile su API-Sports o RapidAPI) è l'approccio ideale.

Ecco gli endpoint e il workflow consigliato:

1. **Recupero delle Leghe (Top 50)**:
   - Endpoint: `GET /leagues`
   - Uso: Filtrare le competizioni desiderate. Restituisce anche tutte le `seasons` disponibili per ciascuna lega. Molte leghe storiche europee hanno dati molto profondi.

2. **Recupero Team e Info Geografiche**:
   - Endpoint: `GET /teams?league={id}&season={year}`
   - Uso: Ottenere i nomi esatti, l'ID univoco dei team e, soprattutto, la **Città** o lo stadio di riferimento (da cui estrarre la città per individuare il Bonus Derby $D$).

3. **Recupero Storico Classifiche (`season_final_standing`)**:
   - Endpoint: `GET /standings?league={id}&season={year}`
   - Uso: Estrarre il `rank` finale (posizione in classifica) di ogni squadra per ogni anno, per popolare il campo `season_final_standing`.

4. **Recupero Incontri e Risultati (`matches_history`)**:
   - Endpoint: `GET /fixtures?league={id}&season={year}`
   - Uso: Scaricare la lista delle partite. I dati conterranno `fixture.date`, `teams.home.name`, `teams.away.name`, `goals.home` e `goals.away`. Sono i dati più certi e coprono l'intero storico.

5. **Recupero Palmarès (`total_major_trophies`)**:
   - Endpoint: `GET /trophies?player={id}` o `GET /coach={id}` (API-Football non ha sempre un endpoint diretto per i trofei storici aggregati dei team, per cui i dati di `total_major_trophies` andrebbero integrati tramite scraping da Wikipedia/RSSSF o con un set di dati statico curato a mano, essendo i titoli una metrica che si aggiorna lentamente).

---

## 3. Guida all'Uso dello Script Python

Il file `rivalry_model.py` contiene la classe `RivalryIndexCalculator` che permette di calcolare in modo vettorializzato l'Indice di Rivalità. 
Per usarlo:

```python
import pandas as pd
from rivalry_model import RivalryIndexCalculator

# 1. Carica i dati dai tuoi CSV / DB
matches_df = pd.read_csv('matches_history.csv')
teams_df = pd.read_csv('teams_metadata.csv')

# 2. Inizializza il calcolatore con i pesi
# w_c = Competitività (C)
# w_p = Posta in Palio/Gerarchia (P)
# w_l = Longevità (L)
# w_t = Prestigio/Pressione (T)
calc = RivalryIndexCalculator(w_c=0.25, w_p=0.25, w_l=0.25, w_t=0.25)

# 3. Calcola l'indice
results = calc.compute_rivalry_index(matches_df, teams_df)

# 4. Modifica i pesi a caldo se necessario (es. diamo più importanza a Longevità e Prestigio)
calc.set_weights(w_c=0.1, w_p=0.1, w_l=0.4, w_t=0.4)
new_results = calc.compute_rivalry_index(matches_df, teams_df)
```
