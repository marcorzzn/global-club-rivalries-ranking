import json
import csv
import sys

def run():
    print("Migrating raw_rivalries to V2 format...")
    
    with open('data/clubs.json', 'r', encoding='utf-8') as f:
        clubs = json.load(f)
        
    slug_map = {c['official_name']: c['slug'] for c in clubs}
    
    with open('data/raw_rivalries.json', 'r', encoding='utf-8') as f:
        raw = json.load(f)
        
    new_rivs = []
    failures = []
    
    for r in raw:
        na = r['club_a']['name']
        nb = r['club_b']['name']
        sa = slug_map.get(na)
        sb = slug_map.get(nb)
        
        if not sa or not sb:
            failed_club = na if not sa else nb
            failures.append({'club_a': na, 'club_b': nb, 'missing_slug_for': failed_club})
            continue
            
        sorted_slugs = sorted([sa, sb])
        rivalry_id = f"{sorted_slugs[0]}--{sorted_slugs[1]}"
        
        # Helper to extract scores
        def get_sourced(key, old_key=None, is_dict=False, dict_key='score'):
            val = None
            if old_key is None: old_key = key
            
            if is_dict:
                if isinstance(r.get(old_key), dict):
                    val = r[old_key].get(dict_key)
            else:
                val = r.get(old_key)
                
            return {"value": val, "source": None, "retrieved_at": None}

        # Build new structure
        new_r = {
            "rivalry_id": rivalry_id,
            "club_a_slug": sa,
            "club_b_slug": sb,
            "rivalry_name": r.get('rivalry_name'),
            "city_derby": r.get('city_derby', False),
            "confederation": r.get('confederation', 'UEFA'),
            "h2h": {
                "total": r.get('h2h', {}).get('total') if isinstance(r.get('h2h'), dict) else None,
                "w_a": r.get('h2h', {}).get('w_a') if isinstance(r.get('h2h'), dict) else None,
                "d": r.get('h2h', {}).get('d') if isinstance(r.get('h2h'), dict) else None,
                "w_b": r.get('h2h', {}).get('w_b') if isinstance(r.get('h2h'), dict) else None,
                "source": None,
                "retrieved_at": None
            },
            "stadium": {
                "a": r.get('stadium', {}).get('a') if isinstance(r.get('stadium'), dict) else None,
                "b": r.get('stadium', {}).get('b') if isinstance(r.get('stadium'), dict) else None,
                "source": None,
                "retrieved_at": None
            },
            "h_club": {
                "a": r.get('h_club', {}).get('a') if isinstance(r.get('h_club'), dict) else None,
                "b": r.get('h_club', {}).get('b') if isinstance(r.get('h_club'), dict) else None,
                "source": None,
                "retrieved_at": None
            },
            "h_dom": get_sourced('h_dom', 'h_dom_score'),
            "h_cont": get_sourced('h_cont', 'h_cont_score'),
            "i_soc": get_sourced('i_soc'),
            "i_name": get_sourced('i_name'),
            "attendance": get_sourced('attendance', is_dict=True, dict_key='median')
        }
        
        new_rivs.append(new_r)
        
    # Deduplicate rivalry_ids
    unique_rivs = {riv['rivalry_id']: riv for riv in new_rivs}.values()
    
    with open('data/rivalries.json', 'w', encoding='utf-8') as f:
        json.dump(list(unique_rivs), f, indent=2)
        
    print(f"Total raw rivalries: {len(raw)}")
    print(f"Successfully migrated: {len(unique_rivs)}")
    print(f"Failed (club not found): {len(failures)}")
    if failures:
        print(f"Failed club names: {[f['missing_slug_for'] for f in failures]}")
        with open('migration_failures.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['club_a', 'club_b', 'missing_slug_for'])
            writer.writeheader()
            writer.writerows(failures)

if __name__ == '__main__':
    run()
