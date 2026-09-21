import json
import os

leagues_data = {
  "source": "Opta Power Rankings (theanalyst.com)",
  "season": "2024-25",
  "snapshot_date": "2025-09-21",
  "note": "Rankings based on average Elo rating of clubs within each competition",
  "leagues": [
    {"rank": 1, "name": "Premier League", "country": "England", "confederation": "UEFA"},
    {"rank": 2, "name": "Serie A", "country": "Italy", "confederation": "UEFA"},
    {"rank": 3, "name": "Bundesliga", "country": "Germany", "confederation": "UEFA"},
    {"rank": 4, "name": "La Liga", "country": "Spain", "confederation": "UEFA"},
    {"rank": 5, "name": "Ligue 1", "country": "France", "confederation": "UEFA"},
    {"rank": 6, "name": "Brasileirão Série A", "country": "Brazil", "confederation": "CONMEBOL"},
    {"rank": 7, "name": "Primeira Liga", "country": "Portugal", "confederation": "UEFA"},
    {"rank": 8, "name": "Eredivisie", "country": "Netherlands", "confederation": "UEFA"},
    {"rank": 9, "name": "Belgian Pro League", "country": "Belgium", "confederation": "UEFA"},
    {"rank": 10, "name": "Major League Soccer", "country": "USA", "confederation": "CONCACAF"},
    {"rank": 11, "name": "EFL Championship", "country": "England", "confederation": "UEFA"},
    {"rank": 12, "name": "Scottish Premiership", "country": "Scotland", "confederation": "UEFA"},
    {"rank": 13, "name": "Süper Lig", "country": "Turkey", "confederation": "UEFA"},
    {"rank": 14, "name": "Russian Premier League", "country": "Russia", "confederation": "UEFA"},
    {"rank": 15, "name": "Argentine Primera División", "country": "Argentina", "confederation": "CONMEBOL"},
    {"rank": 16, "name": "Liga MX", "country": "Mexico", "confederation": "CONCACAF"},
    {"rank": 17, "name": "Super League Greece", "country": "Greece", "confederation": "UEFA"},
    {"rank": 18, "name": "Czech First League", "country": "Czech Republic", "confederation": "UEFA"},
    {"rank": 19, "name": "Austrian Football Bundesliga", "country": "Austria", "confederation": "UEFA"},
    {"rank": 20, "name": "Swiss Super League", "country": "Switzerland", "confederation": "UEFA"},
    {"rank": 21, "name": "Ukrainian Premier League", "country": "Ukraine", "confederation": "UEFA"},
    {"rank": 22, "name": "Danish Superliga", "country": "Denmark", "confederation": "UEFA"},
    {"rank": 23, "name": "Eliteserien", "country": "Norway", "confederation": "UEFA"},
    {"rank": 24, "name": "Allsvenskan", "country": "Sweden", "confederation": "UEFA"},
    {"rank": 25, "name": "Ekstraklasa", "country": "Poland", "confederation": "UEFA"},
    {"rank": 26, "name": "J1 League", "country": "Japan", "confederation": "AFC"},
    {"rank": 27, "name": "K League 1", "country": "South Korea", "confederation": "AFC"},
    {"rank": 28, "name": "Saudi Pro League", "country": "Saudi Arabia", "confederation": "AFC"},
    {"rank": 29, "name": "Categoría Primera A", "country": "Colombia", "confederation": "CONMEBOL"},
    {"rank": 30, "name": "Chilean Primera División", "country": "Chile", "confederation": "CONMEBOL"},
    {"rank": 31, "name": "Uruguayan Primera División", "country": "Uruguay", "confederation": "CONMEBOL"},
    {"rank": 32, "name": "Ecuadorian Serie A", "country": "Ecuador", "confederation": "CONMEBOL"},
    {"rank": 33, "name": "Peruvian Primera División", "country": "Peru", "confederation": "CONMEBOL"},
    {"rank": 34, "name": "Paraguayan Primera División", "country": "Paraguay", "confederation": "CONMEBOL"},
    {"rank": 35, "name": "Bolivian Primera División", "country": "Bolivia", "confederation": "CONMEBOL"},
    {"rank": 36, "name": "Egyptian Premier League", "country": "Egypt", "confederation": "CAF"},
    {"rank": 37, "name": "South African Premier Division", "country": "South Africa", "confederation": "CAF"},
    {"rank": 38, "name": "Botola Pro", "country": "Morocco", "confederation": "CAF"},
    {"rank": 39, "name": "Tunisian Ligue Professionnelle 1", "country": "Tunisia", "confederation": "CAF"},
    {"rank": 40, "name": "Algerian Ligue Professionnelle 1", "country": "Algeria", "confederation": "CAF"},
    {"rank": 41, "name": "A-League Men", "country": "Australia", "confederation": "AFC"},
    {"rank": 42, "name": "Persian Gulf Pro League", "country": "Iran", "confederation": "AFC"},
    {"rank": 43, "name": "UAE Pro League", "country": "United Arab Emirates", "confederation": "AFC"},
    {"rank": 44, "name": "Qatar Stars League", "country": "Qatar", "confederation": "AFC"},
    {"rank": 45, "name": "Thai League 1", "country": "Thailand", "confederation": "AFC"},
    {"rank": 46, "name": "V.League 1", "country": "Vietnam", "confederation": "AFC"},
    {"rank": 47, "name": "Liga 1", "country": "Indonesia", "confederation": "AFC"},
    {"rank": 48, "name": "Malaysia Super League", "country": "Malaysia", "confederation": "AFC"},
    {"rank": 49, "name": "Indian Super League", "country": "India", "confederation": "AFC"},
    {"rank": 50, "name": "Costa Rican Primera División", "country": "Costa Rica", "confederation": "CONCACAF"}
  ]
}

os.makedirs('data', exist_ok=True)
with open('data/leagues_opta.json', 'w', encoding='utf-8') as f:
    json.dump(leagues_data, f, ensure_ascii=False, indent=2)

print(f"Generated data/leagues_opta.json with {len(leagues_data['leagues'])} leagues.")
