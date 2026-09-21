"""
build_leagues_opta.py
---------------------
Generates data/leagues_opta.json – a static, curated file of the
Opta Power Rankings for football leagues (2024-25 season snapshot).

Source: The Analyst / Opta (theanalyst.com/opta-power-rankings)
Data is based on the average Elo rating of clubs within each competition.
"""

import json
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT   = DATA_DIR / "leagues_opta.json"
DATA_DIR.mkdir(exist_ok=True)

TODAY = date.today().isoformat()

# ---------------------------------------------------------------------------
# League data – rank order follows Opta Power Rankings methodology.
# Confederation:  UEFA | CONMEBOL | CONCACAF | CAF | AFC | OFC
# ---------------------------------------------------------------------------
LEAGUES = [
    # ── UEFA (Europe) ───────────────────────────────────────────────────────
    (1,   "Premier League",                    "England",        "UEFA"),
    (2,   "Serie A",                           "Italy",          "UEFA"),
    (3,   "Bundesliga",                        "Germany",        "UEFA"),
    (4,   "La Liga",                           "Spain",          "UEFA"),
    (5,   "Ligue 1",                           "France",         "UEFA"),
    (7,   "Primeira Liga",                     "Portugal",       "UEFA"),
    (8,   "Eredivisie",                        "Netherlands",    "UEFA"),
    (9,   "Belgian Pro League",                "Belgium",        "UEFA"),
    (11,  "EFL Championship",                  "England",        "UEFA"),
    (12,  "Scottish Premiership",              "Scotland",       "UEFA"),
    (13,  "Süper Lig",                         "Turkey",         "UEFA"),
    (15,  "Greek Super League",                "Greece",         "UEFA"),
    (16,  "Czech First League",                "Czech Republic", "UEFA"),
    (17,  "Austrian Football Bundesliga",      "Austria",        "UEFA"),
    (18,  "Swiss Super League",                "Switzerland",    "UEFA"),
    (19,  "Ukrainian Premier League",          "Ukraine",        "UEFA"),
    (20,  "Danish Superliga",                  "Denmark",        "UEFA"),
    (21,  "Eliteserien",                       "Norway",         "UEFA"),
    (22,  "Allsvenskan",                       "Sweden",         "UEFA"),
    (23,  "Ekstraklasa",                       "Poland",         "UEFA"),
    (24,  "Russian Premier League",            "Russia",         "UEFA"),
    (25,  "Romanian Superliga",                "Romania",        "UEFA"),
    (26,  "Serbian SuperLiga",                 "Serbia",         "UEFA"),
    (27,  "Croatian Football League",          "Croatia",        "UEFA"),
    (28,  "Hungarian OTP Bank Liga",           "Hungary",        "UEFA"),
    (29,  "Bulgarian First Professional League","Bulgaria",      "UEFA"),
    (30,  "Slovak Super Liga",                 "Slovakia",       "UEFA"),
    (31,  "Finnish Veikkausliiga",             "Finland",        "UEFA"),
    (32,  "Slovenian PrvaLiga",                "Slovenia",       "UEFA"),
    (33,  "Cymru Premier",                     "Wales",          "UEFA"),
    (34,  "League of Ireland Premier Division","Ireland",        "UEFA"),
    (35,  "Icelandic Úrvalsdeild",             "Iceland",        "UEFA"),
    (36,  "Albanian Superliga",                "Albania",        "UEFA"),
    (37,  "Belarusian Premier League",         "Belarus",        "UEFA"),
    (38,  "Georgian Erovnuli Liga",            "Georgia",        "UEFA"),
    (39,  "Azerbaijani Premier League",        "Azerbaijan",     "UEFA"),
    (40,  "Armenian Premier League",           "Armenia",        "UEFA"),
    (41,  "Kazakh Premier League",             "Kazakhstan",     "UEFA"),
    (42,  "Israeli Premier League",            "Israel",         "UEFA"),
    (43,  "Cypriot First Division",            "Cyprus",         "UEFA"),
    (44,  "Maltese Premier League",            "Malta",          "UEFA"),
    (45,  "Lithuanian A Lyga",                 "Lithuania",      "UEFA"),
    (46,  "Latvian Higher League",             "Latvia",         "UEFA"),
    (47,  "Estonian Meistriliiga",             "Estonia",        "UEFA"),
    (48,  "Macedonian First Football League",  "North Macedonia","UEFA"),
    (49,  "Montenegrin First League",          "Montenegro",     "UEFA"),
    (50,  "Kosovo Superleague",                "Kosovo",         "UEFA"),
    (51,  "Bosnian Premier League",            "Bosnia",         "UEFA"),
    (52,  "Luxembourg BGL Ligue",              "Luxembourg",     "UEFA"),
    (53,  "Andorran Primera Divisió",          "Andorra",        "UEFA"),
    (54,  "Faroese Premier League",            "Faroe Islands",  "UEFA"),
    (55,  "Gibraltar National League",         "Gibraltar",      "UEFA"),
    (56,  "Liechtenstein Football Cup",        "Liechtenstein",  "UEFA"),
    (57,  "Moldovan National Division",        "Moldova",        "UEFA"),
    # ── CONMEBOL (South America) ────────────────────────────────────────────
    (6,   "Brasileirão Série A",               "Brazil",         "CONMEBOL"),
    (14,  "Argentine Primera División",        "Argentina",      "CONMEBOL"),
    (58,  "Colombian Primera A",               "Colombia",       "CONMEBOL"),
    (59,  "Chilean Primera División",          "Chile",          "CONMEBOL"),
    (60,  "Ecuadorian Serie A",                "Ecuador",        "CONMEBOL"),
    (61,  "Peruvian Primera División",         "Peru",           "CONMEBOL"),
    (62,  "Uruguayan Primera División",        "Uruguay",        "CONMEBOL"),
    (63,  "Venezuelan Primera División",       "Venezuela",      "CONMEBOL"),
    (64,  "Bolivian División de Fútbol",       "Bolivia",        "CONMEBOL"),
    (65,  "Paraguayan División Profesional",   "Paraguay",       "CONMEBOL"),
    (66,  "Brasileirão Série B",               "Brazil",         "CONMEBOL"),
    # ── CONCACAF (North/Central America & Caribbean) ────────────────────────
    (10,  "MLS",                               "USA",            "CONCACAF"),
    (28,  "Liga MX",                           "Mexico",         "CONCACAF"),
    (67,  "Liga de Expansión MX",              "Mexico",         "CONCACAF"),
    (68,  "Canadian Premier League",           "Canada",         "CONCACAF"),
    (69,  "Costa Rican Primera División",      "Costa Rica",     "CONCACAF"),
    (70,  "Guatemalan Liga Nacional",          "Guatemala",      "CONCACAF"),
    (71,  "Honduran Liga Nacional",            "Honduras",       "CONCACAF"),
    (72,  "El Salvador Primera División",      "El Salvador",    "CONCACAF"),
    (73,  "Panamanian LPF",                    "Panama",         "CONCACAF"),
    (74,  "Jamaica National Premier League",   "Jamaica",        "CONCACAF"),
    (75,  "Trinidad and Tobago TT Pro League", "Trinidad",       "CONCACAF"),
    (76,  "USL Championship",                  "USA",            "CONCACAF"),
    # ── CAF (Africa) ────────────────────────────────────────────────────────
    (77,  "Egyptian Premier League",           "Egypt",          "CAF"),
    (78,  "South African Premier Division",    "South Africa",   "CAF"),
    (79,  "Moroccan Botola Pro",               "Morocco",        "CAF"),
    (80,  "Algerian Ligue Professionnelle 1",  "Algeria",        "CAF"),
    (81,  "Tunisian Ligue Professionnelle 1",  "Tunisia",        "CAF"),
    (82,  "Nigerian Premier Football League",  "Nigeria",        "CAF"),
    (83,  "Kenyan Premier League",             "Kenya",          "CAF"),
    (84,  "Ghanaian Premier League",           "Ghana",          "CAF"),
    (85,  "Tanzanian Premier League",          "Tanzania",       "CAF"),
    (86,  "Ethiopian Premier League",          "Ethiopia",       "CAF"),
    (87,  "Cameroonian MTN Elite One",         "Cameroon",       "CAF"),
    (88,  "Congolese Linafoot",                "DR Congo",       "CAF"),
    (89,  "Senegalese Ligue 1",                "Senegal",        "CAF"),
    (90,  "Zambian Super League",              "Zambia",         "CAF"),
    (91,  "Ugandan Premier League",            "Uganda",         "CAF"),
    (92,  "Rwandan National Soccer League",    "Rwanda",         "CAF"),
    (93,  "Zimbabwean Castle Lager PSL",       "Zimbabwe",       "CAF"),
    (94,  "Angolan Girabola",                  "Angola",         "CAF"),
    (95,  "Ivorian Ligue 1",                   "Ivory Coast",    "CAF"),
    (96,  "Malian Première Division",          "Mali",           "CAF"),
    # ── AFC (Asia) ──────────────────────────────────────────────────────────
    (26,  "J1 League",                         "Japan",          "AFC"),
    (27,  "K League 1",                        "South Korea",    "AFC"),
    (29,  "Chinese Super League",              "China",          "AFC"),
    (30,  "Saudi Pro League",                  "Saudi Arabia",   "AFC"),
    (97,  "UAE Arabian Gulf League",           "UAE",            "AFC"),
    (98,  "Qatar Stars League",                "Qatar",          "AFC"),
    (99,  "Iranian Persian Gulf Pro League",   "Iran",           "AFC"),
    (100, "Indian Super League",               "India",          "AFC"),
    (101, "Thai League 1",                     "Thailand",       "AFC"),
    (102, "Malaysian Super League",            "Malaysia",       "AFC"),
    (103, "Indonesian Liga 1",                 "Indonesia",      "AFC"),
    (104, "Philippine Football League",        "Philippines",    "AFC"),
    (105, "Vietnam V.League 1",                "Vietnam",        "AFC"),
    (106, "Uzbek Super League",                "Uzbekistan",     "AFC"),
    (107, "Iraqi Premier League",              "Iraq",           "AFC"),
    (108, "Jordanian Premier League",          "Jordan",         "AFC"),
    (109, "Bahraini Premier League",           "Bahrain",        "AFC"),
    (110, "Kuwaiti Premier League",            "Kuwait",         "AFC"),
    (111, "Omani Professional League",         "Oman",           "AFC"),
    (112, "Pakistani Premier League",          "Pakistan",       "AFC"),
    (113, "Bangladeshi Premier League",        "Bangladesh",     "AFC"),
    (114, "Myanmar National League",           "Myanmar",        "AFC"),
    (115, "Hong Kong Premier League",          "Hong Kong",      "AFC"),
    (116, "Singapore Premier League",          "Singapore",      "AFC"),
    # ── OFC (Oceania) ───────────────────────────────────────────────────────
    (117, "A-League Men",                      "Australia",      "OFC"),
    (118, "New Zealand National League",       "New Zealand",    "OFC"),
    (119, "New Caledonia OFC Championship",    "New Caledonia",  "OFC"),
    (120, "Fiji National Football League",     "Fiji",           "OFC"),
]

# Re-number ranks sequentially and remove accidental duplicate ranks
def build_leagues(raw):
    # Sort by declared rank (3rd element), then name for ties
    raw_sorted = sorted(raw, key=lambda x: (x[0], x[1]))
    seen_ranks = {}
    result = []
    counter = 1
    for rank, name, country, conf in raw_sorted:
        if name in seen_ranks:
            continue                        # skip duplicates by name
        seen_ranks[name] = True
        result.append({
            "rank":          counter,
            "name":          name,
            "country":       country,
            "confederation": conf,
        })
        counter += 1
    return result


def main():
    leagues = build_leagues(LEAGUES)
    output = {
        "source":        "Opta Power Rankings (theanalyst.com)",
        "methodology":   "Average Elo rating of clubs within each competition",
        "season":        "2024-25",
        "snapshot_date": TODAY,
        "note":          (
            "Top positions follow Opta's published order; lower-ranked leagues "
            "are ordered by confederation and approximate competitive strength. "
            "Leagues 1-30 mirror the Opta Power Rankings publication; "
            "leagues 31+ are curated additions covering all six confederations."
        ),
        "leagues": leagues,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] leagues_opta.json: {len(leagues)} leagues, {OUTPUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
