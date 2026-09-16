import json
import os
import csv
import time
import requests
import re

def run():
    print("Populating missing logos via Wikidata SPARQL...")
    with open('data/clubs.json', 'r', encoding='utf-8') as f:
        clubs = json.load(f)

    headers = {
        'User-Agent': 'MWI-50-Ultra-Bot/1.0 (Editorial)',
        'Accept': 'application/sparql-results+json'
    }
    
    endpoint = "https://query.wikidata.org/sparql"
    
    assigned = 0
    manual_queue = []

    for c in clubs:
        if c.get('logo_url'):
            continue
            
        slug = c['slug']
        official_name = c['official_name']
        search_name = c.get('search_name', official_name)
        
        # We will try a robust text search in SPARQL
        # Looking for P31=Q476028 (football club) and label matching
        # To avoid SPARQL injection/errors, we'll strip quotes
        safe_name = search_name.replace('"', '').replace("'", "")
        
        query = f"""
        SELECT ?item ?logo ?seal ?arms ?image WHERE {{
          ?item wdt:P31/wdt:P279* wd:Q476028.
          ?item rdfs:label ?label.
          FILTER(CONTAINS(LCASE(?label), LCASE("{safe_name}")) || CONTAINS(LCASE(?label), LCASE("{official_name.replace('"', '')}")))
          OPTIONAL {{ ?item wdt:P154 ?logo. }}
          OPTIONAL {{ ?item wdt:P158 ?seal. }}
          OPTIONAL {{ ?item wdt:P94 ?arms. }}
          OPTIONAL {{ ?item wdt:P18 ?image. }}
        }}
        LIMIT 5
        """
        
        success = False
        try:
            r = requests.get(endpoint, headers=headers, params={'query': query}, timeout=15)
            if r.status_code == 200:
                results = r.json().get('results', {}).get('bindings', [])
                
                # If exactly 1 match or if multiple matches resolve to same item
                unique_items = list(set([res['item']['value'] for res in results]))
                
                if len(unique_items) == 1:
                    # Pick the best image property
                    best_img = None
                    for res in results:
                        if 'logo' in res: best_img = res['logo']['value']
                        elif 'seal' in res and not best_img: best_img = res['seal']['value']
                        elif 'arms' in res and not best_img: best_img = res['arms']['value']
                        
                    if best_img:
                        c['logo_url'] = best_img
                        c['logo_source'] = 'wikidata'
                        c['remote_id'] = unique_items[0].split('/')[-1] # the Q-ID
                        c['logo_license'] = 'CC-BY-SA or Public Domain (Wikimedia Commons)'
                        c['attribution'] = f"Badge from Wikimedia Commons via Wikidata {c['remote_id']}"
                        assigned += 1
                        success = True
            time.sleep(1)
        except Exception as e:
            print(f"Error querying Wikidata for {slug}: {e}")
            
        if not success:
            manual_queue.append({'slug': slug, 'official_name': official_name, 'country': c.get('country', '')})

    with open('data/clubs.json', 'w', encoding='utf-8') as f:
        json.dump(clubs, f, indent=2)

    if manual_queue:
        with open('logo_review_queue_manual.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['slug', 'official_name', 'country'])
            writer.writeheader()
            writer.writerows(manual_queue)

    print(f"Assigned {assigned} logos via Wikidata.")
    print(f"{len(manual_queue)} clubs sent to manual queue.")

if __name__ == '__main__':
    run()
