import json
with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)

for r in rivs:
    if 'stadium' in r:
        a = r['stadium'].get('a')
        b = r['stadium'].get('b')
        if isinstance(a, dict) and isinstance(a.get('value'), dict):
            # Fix it
            r['stadium']['a']['value'] = a['value'].get('a')
        if isinstance(b, dict) and isinstance(b.get('value'), dict):
            r['stadium']['b']['value'] = b['value'].get('b')

with open('data/rivalries.json', 'w', encoding='utf-8') as f:
    json.dump(rivs, f, indent=2)

print('Fixed stadiums.')
