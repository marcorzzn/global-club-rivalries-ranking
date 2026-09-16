import json
with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)

for r in rivs:
    if 'stadium' in r:
        a_val = r['stadium'].get('a')
        b_val = r['stadium'].get('b')
        src = r['stadium'].get('source')
        ret = r['stadium'].get('retrieved_at')
        
        # Extract value if nested
        if isinstance(a_val, dict):
            src = src or a_val.get('source')
            ret = ret or a_val.get('retrieved_at')
            a_val = a_val.get('value')
        if isinstance(b_val, dict):
            src = src or b_val.get('source')
            ret = ret or b_val.get('retrieved_at')
            b_val = b_val.get('value')
            
        r['stadium'] = {
            'a': a_val,
            'b': b_val,
            'source': src,
            'retrieved_at': ret
        }

with open('data/rivalries.json', 'w', encoding='utf-8') as f:
    json.dump(rivs, f, indent=2)

print('Fixed stadiums completely.')
