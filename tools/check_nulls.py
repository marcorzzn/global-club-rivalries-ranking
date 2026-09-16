import json
with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)

for r in rivs:
    rid = r['rivalry_id']
    missing = []
    
    mc = r.get('match_context', {})
    if mc is None:
        missing.append('match_context')
    else:
        for k in ['continental_finals', 'top5_league', 'top10_league', 'national_cups', 'state_regional']:
            if mc.get(k, {}).get('value') is None: missing.append(f'match_context.{k}')
        
    for k in ['h_dom', 'h_cont', 'h_club', 'i_soc', 'i_name', 'attendance']:
        if r.get(k) is None or r.get(k, {}).get('value') is None: missing.append(k)
        
    st = r.get('stadium')
    if st is None:
        missing.append('stadium')
    else:
        if st.get('a') is None or (isinstance(st.get('a'), dict) and st.get('a').get('value') is None): missing.append('stadium.a')
        if st.get('b') is None or (isinstance(st.get('b'), dict) and st.get('b').get('value') is None): missing.append('stadium.b')
    
    if missing:
        print(f'{rid} is missing: {missing}')
print('Validation complete.')
