import json
with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)

for r in rivs:
    print(r['rivalry_id'])
    print(r['stadium'])
    break
