import json
import csv
import requests

def run():
    print("Populating missing logos via Wikipedia API...")
    with open('data/clubs.json', 'r', encoding='utf-8') as f:
        clubs = json.load(f)

    headers = {'User-Agent': 'MWI-50-Ultra-Bot/1.0'}
    
    assigned = 0
    manual_queue = []

    for c in clubs:
        if c.get('logo_url'):
            continue
            
        slug = c['slug']
        search_name = c['official_name']
        
        # English wikipedia fallback
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={search_name}"
        try:
            r = requests.get(url, headers=headers, timeout=5)
            pages = r.json().get('query', {}).get('pages', {})
            page = list(pages.values())[0]
            
            if 'original' in page:
                c['logo_url'] = page['original']['source']
                c['logo_source'] = 'wikipedia'
                c['remote_id'] = str(page.get('pageid', ''))
                c['logo_license'] = 'Fair Use or Public Domain (Wikimedia)'
                c['attribution'] = f"Badge via Wikipedia en:{search_name}"
                assigned += 1
            else:
                manual_queue.append({'slug': slug, 'official_name': search_name})
        except Exception as e:
            manual_queue.append({'slug': slug, 'official_name': search_name})

    with open('data/clubs.json', 'w', encoding='utf-8') as f:
        json.dump(clubs, f, indent=2)

    if manual_queue:
        with open('logo_review_queue_manual.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['slug', 'official_name'])
            writer.writeheader()
            writer.writerows(manual_queue)

    print(f"Assigned {assigned} logos via Wikipedia.")
    print(f"{len(manual_queue)} clubs sent to manual queue.")

if __name__ == '__main__':
    run()
