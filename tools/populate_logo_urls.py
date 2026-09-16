import json
import os
import csv
import time
import requests

def run():
    print("Populating logo URLs via TheSportsDB...")
    with open('data/clubs.json', 'r', encoding='utf-8') as f:
        clubs = json.load(f)

    headers = {'User-Agent': 'MWI-50-Ultra-Bot/1.0 (Editorial)'}
    
    assigned = 0
    review_queue = []
    
    os.makedirs('cache', exist_ok=True)

    for c in clubs:
        if c.get('logo_url'):
            continue
            
        slug = c['slug']
        search_name = c.get('search_name', '')
        country = c.get('country', '')
        
        cache_file = f"cache/{slug}.json"
        
        data = None
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as cf:
                data = json.load(cf)
        else:
            url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={search_name}"
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    with open(cache_file, 'w', encoding='utf-8') as cf:
                        json.dump(data, cf)
                time.sleep(0.7)
            except Exception as e:
                print(f"Error fetching {slug}: {e}")
                data = None

        if data and data.get('teams'):
            # Filter by country if country is known
            candidates = data['teams']
            if country:
                # Basic matching (TheSportsDB country names might differ slightly, e.g. "USA" vs "United States")
                # But we do a simple substring match
                filtered = [t for t in candidates if t.get('strCountry') and country.lower() in t['strCountry'].lower() or t['strCountry'].lower() in country.lower()]
                if len(filtered) > 0:
                    candidates = filtered
            
            if len(candidates) == 1:
                t = candidates[0]
                if t.get('strBadge'):
                    c['logo_url'] = t['strBadge']
                    c['logo_source'] = 'thesportsdb'
                    c['remote_id'] = t.get('idTeam')
                    c['logo_license'] = '© club / TheSportsDB community'
                    c['attribution'] = 'Badge via TheSportsDB'
                    assigned += 1
                    continue
        
        # If we reach here, zero or multiple candidates, or no badge
        review_queue.append({'slug': slug, 'official_name': c['official_name'], 'country': country})

    with open('data/clubs.json', 'w', encoding='utf-8') as f:
        json.dump(clubs, f, indent=2)

    if review_queue:
        with open('logo_review_queue.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['slug', 'official_name', 'country'])
            writer.writeheader()
            writer.writerows(review_queue)

    print(f"Assigned {assigned} logos via TheSportsDB.")
    print(f"{len(review_queue)} clubs sent to logo_review_queue.csv.")

if __name__ == '__main__':
    run()
