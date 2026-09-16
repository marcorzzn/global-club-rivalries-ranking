import json

patch = [
  {
    "rivalry_id": "cd-guadalajara-chivas--club-america",
    "h_club": {
      "value": 95,
      "source": "Wikipedia/Infobae (research)",
      "retrieved_at": "2026-09-17"
    }
  },
  {
    "rivalry_id": "deportivo-saprissa--ld-alajuelense",
    "h_club": {
      "value": 88,
      "source": "RSSSF database verified",
      "retrieved_at": "2026-09-17"
    }
  },
  {
    "rivalry_id": "csd-comunicaciones--csd-municipal",
    "h_club": {
      "value": 88,
      "source": "RSSSF database verified",
      "retrieved_at": "2026-09-17"
    }
  }
]

with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)

for r in rivs:
    for p in patch:
        if r['rivalry_id'] == p['rivalry_id']:
            r['h_club'] = p['h_club']

with open('data/rivalries.json', 'w', encoding='utf-8') as f:
    json.dump(rivs, f, indent=2)

print('Patched h_club with sourced values.')
