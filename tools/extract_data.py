"""
MWI Framework - Rivalry Index Calculator
=========================================
A reusable framework for calculating composite rivalry indices
with context-aware weighting and entropy-based balance scoring.

USAGE:
    1. Popola data/rivalries_verified_template.json con dati verificati manualmente
    2. python tools/partial_ranking_v2.py
    3. Output: rankings.json + audit_report.csv

LICENSE: MIT
CASE STUDY: See walkthrough.md for the audit that exposed
           LLM hallucination risks in historical data extraction.
"""

import json
import os
import subprocess
import re
import unicodedata

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def run():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    match = re.search(r'const RIVALRIES = (\[[\s\S]*?\]);\n// --- I18N', html)
    if not match:
        print("Error: RIVALRIES block not found. Checking fallback...")
        match = re.search(r'const RIVALRIES = (\[[\s\S]*?\]);\n// === RIVALRY DATA END ===', html)
        if not match:
            print("Failed to locate JS array.")
            return

    js_data = match.group(1)
    with open('temp_extract.js', 'w', encoding='utf-8') as f:
        f.write('const data = ' + js_data + ';\nconsole.log(JSON.stringify(data));')

    result = subprocess.run(['node', 'temp_extract.js'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Node error:", result.stderr)
        return
        
    rivalries = json.loads(result.stdout)

    clubs = {}
    for r in rivalries:
        for key in ['club_a', 'club_b']:
            c = r[key]
            name = c['name']
            if name not in clubs:
                slug = slugify(name)
                # Strip common prefixes for better slug/code generation
                search_name = name.upper().replace('FC ', '').replace(' FC', '').replace('AC ', '').replace('CA ', '').replace('CLUB ', '').strip()
                clubs[name] = {
                    "slug": slug,
                    "official_name": name,
                    "search_name": search_name,
                    "color": c.get('color', '#000000')
                }
    
    # Generate UNIQUE codes
    used_codes = set()
    for name, c in clubs.items():
        # Try to make a smart 3-letter code from search_name
        letters = re.sub(r'[^A-Z]', '', c['search_name'] + "ABC")
        base_code = letters[:3]
        
        if base_code in used_codes:
            # Fallback to consonants or random
            base_code = letters[0] + letters[2:4]
            if len(base_code) < 3 or base_code in used_codes:
                # brute force unique
                for i in range(1, 999):
                    cand = f"{letters[0]}{i:02d}"
                    if cand not in used_codes:
                        base_code = cand
                        break
                        
        used_codes.add(base_code)
        c['code'] = base_code

    os.makedirs('data', exist_ok=True)
    
    # Sort clubs by slug
    clubs_list = sorted(list(clubs.values()), key=lambda x: x['slug'])
    
    with open('data/clubs.json', 'w', encoding='utf-8') as f:
        json.dump(clubs_list, f, indent=2)

    with open('data/raw_rivalries.json', 'w', encoding='utf-8') as f:
        json.dump(rivalries, f, indent=2)

    print(f"Extraction complete! Found {len(clubs_list)} unique clubs.")
    print("Created data/clubs.json and data/raw_rivalries.json")
    
    if os.path.exists('temp_extract.js'):
        os.remove('temp_extract.js')

if __name__ == '__main__':
    run()
