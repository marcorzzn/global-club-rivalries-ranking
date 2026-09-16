import re
import requests
import time

def run():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    missing = [
      {
        "id": "UEFA_FIO_JUV", "club_a": {"name": "ACF Fiorentina", "short": "FIO", "color": "#4B0082"}, "club_b": {"name": "Juventus FC", "short": "JUV", "color": "#000000"},
        "country": "Italy", "confederation": "UEFA", "rivalry_name": "Rivalità Fiorentina-Juventus", "city_derby": False,
        "h2h": {"total": 95, "w_a": None, "d": None, "w_b": None}, "continuity_blocks": [True, True, True, True, True],
        "h_dom_score": 85, "h_cont_score": 0, "h_club": {"a": 30, "b": 95},
        "i_name": 50, "i_soc": 100, "stadium": {"a": 43147, "b": 41507},
        "attendance": {"coverage": 0, "median": None}, "confidence": "MEDIUM"
      },
      {
        "id": "UEFA_ROM_JUV", "club_a": {"name": "AS Roma", "short": "ASR", "color": "#8B0000"}, "club_b": {"name": "Juventus FC", "short": "JUV", "color": "#000000"},
        "country": "Italy", "confederation": "UEFA", "rivalry_name": "Rivalità Roma-Juventus", "city_derby": False,
        "h2h": {"total": 102, "w_a": None, "d": None, "w_b": None}, "continuity_blocks": [True, True, True, True, True],
        "h_dom_score": 90, "h_cont_score": 0, "h_club": {"a": 40, "b": 95},
        "i_name": 50, "i_soc": 75, "stadium": {"a": 70634, "b": 41507},
        "attendance": {"coverage": 0, "median": None}, "confidence": "MEDIUM"
      },
      {
        "id": "UEFA_ROM_NAP", "club_a": {"name": "AS Roma", "short": "ASR", "color": "#8B0000"}, "club_b": {"name": "SSC Napoli", "short": "NAP", "color": "#1FA4D0"},
        "country": "Italy", "confederation": "UEFA", "rivalry_name": "Derby del Sole", "city_derby": False,
        "h2h": {"total": 98, "w_a": None, "d": None, "w_b": None}, "continuity_blocks": [True, True, True, True, True],
        "h_dom_score": 85, "h_cont_score": 0, "h_club": {"a": 40, "b": 40},
        "i_name": 100, "i_soc": 75, "stadium": {"a": 70634, "b": 54726},
        "attendance": {"coverage": 0, "median": None}, "confidence": "MEDIUM"
      },
      {
        "id": "UEFA_LYO_STE", "club_a": {"name": "Olympique Lyonnais", "short": "LYO", "color": "#FFFFFF"}, "club_b": {"name": "AS Saint-Etienne", "short": "STE", "color": "#008000"},
        "country": "France", "confederation": "UEFA", "rivalry_name": "Derby Rhône-Alpes", "city_derby": False,
        "h2h": {"total": 92, "w_a": None, "d": None, "w_b": None}, "continuity_blocks": [True, True, True, True, True],
        "h_dom_score": 90, "h_cont_score": 0, "h_club": {"a": 70, "b": 70},
        "i_name": 100, "i_soc": 100, "stadium": {"a": 59186, "b": 41965},
        "attendance": {"coverage": 0, "median": None}, "confidence": "MEDIUM"
      },
      {
        "id": "UEFA_LEE_MAN", "club_a": {"name": "Leeds United", "short": "LEE", "color": "#FFFFFF"}, "club_b": {"name": "Manchester United", "short": "MAN", "color": "#DA291C"},
        "country": "England", "confederation": "UEFA", "rivalry_name": "Roses Rivalry", "city_derby": False,
        "h2h": {"total": 65, "w_a": None, "d": None, "w_b": None}, "continuity_blocks": [True, True, False, True, True],
        "h_dom_score": 85, "h_cont_score": 0, "h_club": {"a": 30, "b": 95},
        "i_name": 100, "i_soc": 100, "stadium": {"a": 37792, "b": 74310},
        "attendance": {"coverage": 0, "median": None}, "confidence": "MEDIUM"
      }
    ]

    import json
    new_rivalries_str = ""
    for r in missing:
        # Convert true/false/null manually to lowercase for JS
        r_str = json.dumps(r)
        new_rivalries_str += "  " + r_str + ",\n"

    match = re.search(r'(const RIVALRIES = \[\n)', html)
    if match:
        new_html = html[:match.end()] + new_rivalries_str + html[match.end():]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print('Successfully added missing rivalries')

    # Fetch missing logos
    clubs_to_fetch = {
        "FIO": "Fiorentina",
        "ASR": "AS Roma",
        "LYO": "Olympique Lyonnais",
        "STE": "Saint-Etienne",
        "LEE": "Leeds United"
    }

    for short_name, club_name in clubs_to_fetch.items():
        try:
            search_name = club_name.replace('FC ', '').replace(' FC', '').replace('CF', '').strip()
            url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={search_name}"
            r = requests.get(url, timeout=10)
            data = r.json()
            if data and data.get('teams'):
                badge_url = data['teams'][0].get('strBadge')
                if badge_url:
                    img_data = requests.get(badge_url, timeout=10).content
                    with open(f"logos/{short_name}.png", 'wb') as img_file:
                        img_file.write(img_data)
                    print(f"  -> Saved {short_name}.png")
        except Exception as e:
            print(f"Error fetching {short_name}: {e}")
        time.sleep(0.5)

if __name__ == '__main__':
    run()
