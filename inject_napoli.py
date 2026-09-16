import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_rivalry = """  {
    id: "UEFA_JUV_NAP", club_a: {"name": "Juventus FC", "short": "JUV", "color": "#000000"}, club_b: {"name": "SSC Napoli", "short": "NAP", "color": "#1FA4D0"},
    country: "Italy", confederation: "UEFA", rivalry_name: "Rivalità Juventus-Napoli", city_derby: false,
    h2h: {"total": 105, "w_a": null, "d": null, "w_b": null}, continuity_blocks: [true, true, true, true, true],
    h_dom_score: 95, h_cont_score: 0, h_club: {"a": 95, "b": 40},
    i_name: 50, i_soc: 100, stadium: {"a": 41507, "b": 54726},
    attendance: {"coverage": 0, "median": null}, confidence: "MEDIUM"
  },
"""

match = re.search(r'(const RIVALRIES = \[\n)', html)
if match:
    new_html = html[:match.end()] + new_rivalry + html[match.end():]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print('Successfully added Juventus vs Napoli')
