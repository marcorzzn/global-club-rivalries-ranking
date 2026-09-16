import json

top20_ids = [
    'fc-barcelona--real-madrid',
    'ac-milan--fc-internazionale-milano',
    'ca-boca-juniors--ca-river-plate',
    'club-america--cruz-azul',
    'al-ahly-sc--zamalek-sc',
    'kaizer-chiefs--orlando-pirates',
    'celtic-fc--rangers-fc',
    'arsenal-fc--tottenham-hotspur',
    'liverpool-fc--manchester-united',
    'ac-milan--juventus-fc',
    'fc-internazionale-milano--juventus-fc',
    'atletico-madrid--real-madrid',
    'borussia-dortmund--fc-bayern-munich',
    'as-roma--ss-lazio',
    'fc-porto--sl-benfica',
    'sl-benfica--sporting-cp',
    'afc-ajax--feyenoord-rotterdam',
    'olympiacos-fc--panathinaikos-fc',
    'fenerbahce-sk--galatasaray-sk',
    'cr-flamengo--fluminense-fc',
    'sc-corinthians--se-palmeiras'
]

with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)

trimmed = []
for r in rivs:
    if r['rivalry_id'] in top20_ids:
        # Pialliamo i dati
        clean_r = {
            'rivalry_id': r['rivalry_id'],
            'club_a': r.get('club_a'),
            'club_b': r.get('club_b'),
            'confederation': r.get('confederation', 'UNKNOWN'),
            'h2h': {
                'total': {'value': None, 'source': None},
                'w_a': {'value': None, 'source': None},
                'd': {'value': None, 'source': None},
                'w_b': {'value': None, 'source': None},
                'active_decades': {'value': None, 'source': None}
            },
            'h_dom': {'value': None, 'source': None},
            'h_cont': {'value': None, 'source': None},
            'h_club': {'value': None, 'source': None},
            'i_soc': {'value': None, 'source': None},
            'i_name': {'value': None, 'source': None},
            'stadium': {
                'a': {'value': None, 'source': None},
                'b': {'value': None, 'source': None}
            },
            'attendance': {'value': None, 'source': None},
            'match_context': {
                'continental_finals': {'value': None, 'source': None},
                'top5_league': {'value': None, 'source': None},
                'top10_league': {'value': None, 'source': None},
                'national_cups': {'value': None, 'source': None},
                'state_regional': {'value': None, 'source': None}
            }
        }
        trimmed.append(clean_r)

with open('data/rivalries_verified_template.json', 'w', encoding='utf-8') as f:
    json.dump(trimmed, f, indent=2)

print(f'Template pulito generato con {len(trimmed)} rivalità.')
