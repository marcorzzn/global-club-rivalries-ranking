import json
with open('data/rivalry_schema.json', 'r', encoding='utf-8') as f:
    s = json.load(f)
print(json.dumps(s['properties']['stadium'], indent=2))
