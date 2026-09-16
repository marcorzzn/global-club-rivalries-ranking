import json

TOP_20 = [
    "ca-boca-juniors--ca-river-plate",
    "celtic-fc--rangers-fc",
    "fc-barcelona--real-madrid",
    "ac-milan--fc-internazionale-milano",
    "liverpool-fc--manchester-united",
    "fenerbahce-sk--galatasaray-sk",
    "ca-penarol--club-nacional-de-football",
    "afc-ajax--feyenoord-rotterdam",
    "olympiacos-fc--panathinaikos-fc",
    "al-ahly-sc--zamalek-sc",
    "cr-flamengo--fluminense-fc",
    "arsenal-fc--tottenham-hotspur",
    "as-roma--ss-lazio",
    "borussia-dortmund--fc-schalke-04",
    "cd-guadalajara-chivas--club-america",
    "sl-benfica--sporting-cp",
    "fc-internazionale-milano--juventus-fc",
    "atletico-madrid--real-madrid",
    "gremio-fbpa--sc-internacional",
    "ca-boca-juniors--ca-independiente"
]

def get_raw_h2h(raw_rivs, slug_a, slug_b):
    # This is a bit tricky because raw uses names, but we can just map the slugs
    for r in raw_rivs:
        # Simplification: we know the migration mapped names to slugs. 
        # But we don't have the map here.
        # Let's just find it by finding the one that maps to the same confederation or something.
        pass
    return 0

def run():
    print("Prioritizing rivalries...")
    
    with open('data/rivalries.json', 'r', encoding='utf-8') as f:
        rivs = json.load(f)
        
    with open('data/raw_rivalries.json', 'r', encoding='utf-8') as f:
        raw_rivs = json.load(f)
        
    # Build a lookup from raw_rivalries based on city_derby + confederation + some heuristic?
    # Better: re-run the slug_map from clubs.json
    with open('data/clubs.json', 'r', encoding='utf-8') as f:
        clubs = json.load(f)
    slug_map = {c['official_name']: c['slug'] for c in clubs}
    
    raw_h2h_map = {}
    for r in raw_rivs:
        sa = slug_map.get(r['club_a']['name'])
        sb = slug_map.get(r['club_b']['name'])
        if sa and sb:
            rid = f"{sorted([sa, sb])[0]}--{sorted([sa, sb])[1]}"
            # Some raw have total as int, some don't.
            tot = r.get('h2h', {}).get('total', 0) if isinstance(r.get('h2h'), dict) else 0
            if not isinstance(tot, int): tot = 0
            raw_h2h_map[rid] = tot

    for r in rivs:
        rid = r['rivalry_id']
        tot = raw_h2h_map.get(rid, 0)
        
        if rid in TOP_20:
            priority = 1
        elif tot >= 100:
            priority = 2
        elif r.get('confederation') in ['UEFA', 'CONMEBOL']:
            priority = 3
        else:
            priority = 4
            
        r['priority_tier'] = priority
        r['_raw_h2h_total'] = tot  # Temporary for sorting
        
    # Sort by priority ASC, then raw_h2h_total DESC
    rivs.sort(key=lambda x: (x['priority_tier'], -x['_raw_h2h_total']))
    
    # Clean up the temporary field and flag top 80
    for i, r in enumerate(rivs):
        del r['_raw_h2h_total']
        r['priority'] = True if i < 80 else False
        
    with open('data/priority_queue.json', 'w', encoding='utf-8') as f:
        json.dump(rivs, f, indent=2)
        
    print(f"Priority queue generated: {len(rivs)} items.")
    print(f"Top 80 marked for F3.")
    
if __name__ == '__main__':
    run()
