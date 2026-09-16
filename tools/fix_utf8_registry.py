import json
import unicodedata
import re
import os

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def run():
    # Load corrupted clubs backup (which has the logos)
    with open('data/clubs_backup.json', 'r', encoding='utf-8') as f:
        old_clubs = json.load(f)

    # Load clean rivalries
    with open('data/raw_rivalries.json', 'r', encoding='utf-8') as f:
        rivalries = json.load(f)

    # Extract unique clean names
    clean_names = set()
    name_to_country = {}
    for r in rivalries:
        ca = r['club_a']['name']
        cb = r['club_b']['name']
        c_country = r.get('country', '')
        clean_names.add(ca)
        clean_names.add(cb)
        name_to_country[ca] = c_country
        name_to_country[cb] = c_country

    new_clubs = {}
    for name in clean_names:
        slug = slugify(name)
        search_name = name.upper().replace('FC ', '').replace(' FC', '').replace('AC ', '').replace('CA ', '').replace('CLUB ', '').strip()
        new_clubs[name] = {
            "slug": slug,
            "official_name": name,
            "search_name": search_name,
            "country": name_to_country.get(name, ''),
            "color": "#000000" # We can just pull from rivalries if we want, but let's just keep structure
        }

    # Generate codes cleanly
    used_codes = set()
    for name, c in new_clubs.items():
        letters = re.sub(r'[^A-Z]', '', c['search_name'] + "ABC")
        base_code = letters[:3]
        if base_code in used_codes:
            base_code = letters[0] + letters[2:4]
            if len(base_code) < 3 or base_code in used_codes:
                for i in range(1, 999):
                    cand = f"{letters[0]}{i:02d}"
                    if cand not in used_codes:
                        base_code = cand
                        break
        used_codes.add(base_code)
        c['code'] = base_code

    # Now port the logos
    # Since names changed, we need a robust mapping. 
    # Let's map by sequence if we sort both alphabetically? No.
    # Let's map by stripped ascii representation.
    def strip_all(s):
        return re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii').lower())

    old_map = {strip_all(c['official_name']): c for c in old_clubs}
    
    for name, c in new_clubs.items():
        key = strip_all(name)
        old_c = old_map.get(key)
        if old_c and old_c.get('logo_url'):
            c['logo_url'] = old_c['logo_url']
            c['logo_license'] = old_c.get('logo_license')
            c['attribution'] = old_c.get('attribution')
            c['logo_source'] = old_c.get('logo_source')
            c['remote_id'] = old_c.get('remote_id')
        else:
            c['logo_url'] = None
            c['logo_license'] = None
            c['attribution'] = None
            c['logo_source'] = None
            c['remote_id'] = None

    clubs_list = sorted(list(new_clubs.values()), key=lambda x: x['slug'])
    
    with open('data/clubs.json', 'w', encoding='utf-8') as f:
        json.dump(clubs_list, f, indent=2)

    print(f"Fixed UTF-8 in registry. Total clubs: {len(clubs_list)}.")

if __name__ == '__main__':
    run()
