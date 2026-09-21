import json
import os
import random

def main():
    print("Building ranking data...")
    
    # Let's read the leagues to assign ranks
    try:
        with open('data/leagues_opta.json', 'r', encoding='utf-8') as f:
            leagues_data = json.load(f)
            leagues = leagues_data.get('leagues', [])
    except:
        print("Could not read leagues data. Creating dummy ranking data.")
        leagues = [
            {"rank": 1, "name": "Premier League", "country": "England", "confederation": "UEFA"},
            {"rank": 2, "name": "Serie A", "country": "Italy", "confederation": "UEFA"},
            {"rank": 3, "name": "Bundesliga", "country": "Germany", "confederation": "UEFA"},
            {"rank": 4, "name": "La Liga", "country": "Spain", "confederation": "UEFA"}
        ]
        
    # Helper to find league rank
    def get_league_rank(league_name):
        for l in leagues:
            if l['name'] == league_name:
                return l['rank']
        return 50
        
    # Some famous rivalries for the ranking
    famous_rivalries = [
        {"id": "el_clasico", "name_en": "El Clásico", "name_it": "Il Clásico", "team1": "Real Madrid", "team2": "Barcelona", "country": "Spain", "league": "La Liga", "continent": "Europe", "derby_type": "national", "p_raw": 288, "m_raw": 13, "first_decade": 1900, "last_decade": 2020},
        {"id": "superclasico", "name_en": "Superclásico", "name_it": "Superclásico", "team1": "Boca Juniors", "team2": "River Plate", "country": "Argentina", "league": "Argentine Primera División", "continent": "South America", "derby_type": "city", "p_raw": 260, "m_raw": 11, "first_decade": 1910, "last_decade": 2020},
        {"id": "derby_della_madonnina", "name_en": "Derby della Madonnina", "name_it": "Derby della Madonnina", "team1": "AC Milan", "team2": "Inter Milan", "country": "Italy", "league": "Serie A", "continent": "Europe", "derby_type": "city", "p_raw": 238, "m_raw": 12, "first_decade": 1900, "last_decade": 2020},
        {"id": "derby_d_italia", "name_en": "Derby d'Italia", "name_it": "Derby d'Italia", "team1": "Juventus", "team2": "Inter Milan", "country": "Italy", "league": "Serie A", "continent": "Europe", "derby_type": "national", "p_raw": 251, "m_raw": 12, "first_decade": 1900, "last_decade": 2020},
        {"id": "north_west_derby", "name_en": "North West Derby", "name_it": "Derby del Nord-Ovest", "team1": "Manchester United", "team2": "Liverpool", "country": "England", "league": "Premier League", "continent": "Europe", "derby_type": "regional", "p_raw": 213, "m_raw": 13, "first_decade": 1890, "last_decade": 2020},
        {"id": "old_firm", "name_en": "Old Firm", "name_it": "Old Firm", "team1": "Celtic", "team2": "Rangers", "country": "Scotland", "league": "Scottish Premiership", "continent": "Europe", "derby_type": "city", "p_raw": 437, "m_raw": 14, "first_decade": 1880, "last_decade": 2020},
        {"id": "der_klassiker", "name_en": "Der Klassiker", "name_it": "Der Klassiker", "team1": "Bayern Munich", "team2": "Borussia Dortmund", "country": "Germany", "league": "Bundesliga", "continent": "Europe", "derby_type": "national", "p_raw": 134, "m_raw": 6, "first_decade": 1960, "last_decade": 2020},
        {"id": "paulista_derby", "name_en": "Paulista Derby", "name_it": "Derby Paulista", "team1": "Corinthians", "team2": "Palmeiras", "country": "Brazil", "league": "Brasileirão Série A", "continent": "South America", "derby_type": "city", "p_raw": 378, "m_raw": 11, "first_decade": 1910, "last_decade": 2020},
        {"id": "fla_flu", "name_en": "Fla-Flu", "name_it": "Fla-Flu", "team1": "Flamengo", "team2": "Fluminense", "country": "Brazil", "league": "Brasileirão Série A", "continent": "South America", "derby_type": "city", "p_raw": 448, "m_raw": 12, "first_decade": 1910, "last_decade": 2020},
        {"id": "de_klassieker", "name_en": "De Klassieker", "name_it": "De Klassieker", "team1": "Ajax", "team2": "Feyenoord", "country": "Netherlands", "league": "Eredivisie", "continent": "Europe", "derby_type": "national", "p_raw": 200, "m_raw": 11, "first_decade": 1920, "last_decade": 2020},
        {"id": "north_london_derby", "name_en": "North London Derby", "name_it": "Derby del Nord di Londra", "team1": "Arsenal", "team2": "Tottenham Hotspur", "country": "England", "league": "Premier League", "continent": "Europe", "derby_type": "city", "p_raw": 194, "m_raw": 12, "first_decade": 1900, "last_decade": 2020},
        {"id": "derby_della_capitale", "name_en": "Derby della Capitale", "name_it": "Derby della Capitale", "team1": "Roma", "team2": "Lazio", "country": "Italy", "league": "Serie A", "continent": "Europe", "derby_type": "city", "p_raw": 181, "m_raw": 10, "first_decade": 1920, "last_decade": 2020},
        {"id": "intercontinental_derby", "name_en": "Intercontinental Derby", "name_it": "Derby Intercontinentale", "team1": "Galatasaray", "team2": "Fenerbahçe", "country": "Turkey", "league": "Süper Lig", "continent": "Europe", "derby_type": "city", "p_raw": 398, "m_raw": 12, "first_decade": 1900, "last_decade": 2020},
        {"id": "le_classique", "name_en": "Le Classique", "name_it": "Le Classique", "team1": "Paris Saint-Germain", "team2": "Marseille", "country": "France", "league": "Ligue 1", "continent": "Europe", "derby_type": "national", "p_raw": 106, "m_raw": 6, "first_decade": 1970, "last_decade": 2020},
        {"id": "merseyside_derby", "name_en": "Merseyside Derby", "name_it": "Derby del Merseyside", "team1": "Liverpool", "team2": "Everton", "country": "England", "league": "Premier League", "continent": "Europe", "derby_type": "city", "p_raw": 243, "m_raw": 13, "first_decade": 1890, "last_decade": 2020},
        {"id": "clássico_dos_milhões", "name_en": "Clássico dos Milhões", "name_it": "Clássico dos Milhões", "team1": "Vasco da Gama", "team2": "Flamengo", "country": "Brazil", "league": "Brasileirão Série A", "continent": "South America", "derby_type": "city", "p_raw": 420, "m_raw": 11, "first_decade": 1920, "last_decade": 2020},
        {"id": "el_gran_derbi", "name_en": "El Gran Derbi", "name_it": "Il Gran Derbi", "team1": "Sevilla", "team2": "Real Betis", "country": "Spain", "league": "La Liga", "continent": "Europe", "derby_type": "city", "p_raw": 139, "m_raw": 11, "first_decade": 1910, "last_decade": 2020},
        {"id": "revierderby", "name_en": "Revierderby", "name_it": "Revierderby", "team1": "Borussia Dortmund", "team2": "Schalke 04", "country": "Germany", "league": "Bundesliga", "continent": "Europe", "derby_type": "regional", "p_raw": 159, "m_raw": 10, "first_decade": 1920, "last_decade": 2020},
        {"id": "soweto_derby", "name_en": "Soweto Derby", "name_it": "Derby di Soweto", "team1": "Kaizer Chiefs", "team2": "Orlando Pirates", "country": "South Africa", "league": "South African Premier Division", "continent": "Africa", "derby_type": "city", "p_raw": 178, "m_raw": 6, "first_decade": 1970, "last_decade": 2020},
        {"id": "cairo_derby", "name_en": "Cairo Derby", "name_it": "Derby del Cairo", "team1": "Al Ahly", "team2": "Zamalek", "country": "Egypt", "league": "Egyptian Premier League", "continent": "Africa", "derby_type": "city", "p_raw": 246, "m_raw": 11, "first_decade": 1910, "last_decade": 2020}
    ]
    
    # Calculate League score based on formula L
    max_leagues = len(leagues)
    
    for r in famous_rivalries:
        rank = get_league_rank(r['league'])
        r['league_rank'] = rank
        # Formula L score (0-100)
        r['l_raw'] = ((max_leagues - rank + 1) / max_leagues) * 100
        r['wikipedia_url'] = f"https://en.wikipedia.org/wiki/{r['id']}"
        
    os.makedirs('data', exist_ok=True)
    with open('data/rivalries_ranking.json', 'w', encoding='utf-8') as f:
        json.dump(famous_rivalries, f, ensure_ascii=False, indent=2)
        
    print(f"Generated data/rivalries_ranking.json with {len(famous_rivalries)} entries.")

if __name__ == "__main__":
    main()
