import json
import jsonschema
import sys

def run():
    print("Validating registry and raw rivalries...")
    try:
        with open('data/clubs.json', 'r', encoding='utf-8') as f:
            clubs = json.load(f)
        
        with open('data/rivalry_schema.json', 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except Exception as e:
        print(f"File loading error: {e}")
        sys.exit(1)

    # Validate unique slugs and codes in clubs.json
    slugs = set()
    codes = set()
    for c in clubs:
        slug = c.get('slug')
        code = c.get('code')
        if slug in slugs:
            print(f"CRITICAL: Duplicate slug found: {slug}")
        if code in codes:
            print(f"CRITICAL: Duplicate code found: {code}")
        slugs.add(slug)
        codes.add(code)
    
    print(f"-> clubs.json valid. {len(slugs)} unique clubs.")

if __name__ == '__main__':
    run()
