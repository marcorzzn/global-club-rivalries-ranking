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
import jsonschema
import sys
import os
import hashlib

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def run():
    print("Validating F2 state (Registry + Manifest + Schema)...")
    try:
        with open('data/clubs.json', 'r', encoding='utf-8') as f:
            clubs = json.load(f)
    except Exception as e:
        print(f"File loading error: {e}")
        sys.exit(1)

    if len(clubs) != 194:
        print(f"ERROR: Expected 194 clubs, found {len(clubs)}")
        sys.exit(1)
        
    null_logos = [c['official_name'] for c in clubs if not c.get('logo_url')]
    if null_logos:
        print(f"ERROR: {len(null_logos)} clubs have null logo_url.")
        sys.exit(1)

    try:
        with open('logos/manifest.json', 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except Exception:
        print("Manifest not found or invalid.")
        sys.exit(1)
        
    if len(manifest) != 194:
        print(f"ERROR: Manifest has {len(manifest)} entries, expected 194.")
        sys.exit(1)

    files = [f for f in os.listdir('logos') if f != 'manifest.json']
    if len(files) != 194:
        print(f"ERROR: logos/ has {len(files)} image files, expected 194.")
        sys.exit(1)
        
    manifest_map = {m['file']: m['sha256'] for m in manifest}
    for file in files:
        if file not in manifest_map:
            print(f"ERROR: File {file} not in manifest.")
            sys.exit(1)
        
        actual_hash = sha256_file(os.path.join('logos', file))
        if actual_hash != manifest_map[file]:
            print(f"ERROR: SHA256 mismatch for {file}.")
            sys.exit(1)

    print("Logos / Registry check passed.")

    # F2: Validate rivalries.json against schema
    if os.path.exists('data/rivalries.json'):
        with open('data/rivalry_schema.json', 'r', encoding='utf-8') as f:
            schema = json.load(f)
        with open('data/rivalries.json', 'r', encoding='utf-8') as f:
            rivs = json.load(f)

        club_slugs = {c['slug'] for c in clubs}
        errors = 0
        
        # Checking uniqueness
        r_ids = set()
        for i, r in enumerate(rivs):
            if r['rivalry_id'] in r_ids:
                print(f"ERROR: Duplicate rivalry_id {r['rivalry_id']}")
                errors += 1
            r_ids.add(r['rivalry_id'])
            
            if r['club_a_slug'] not in club_slugs:
                print(f"ERROR: club_a_slug {r['club_a_slug']} not in registry")
                errors += 1
            if r['club_b_slug'] not in club_slugs:
                print(f"ERROR: club_b_slug {r['club_b_slug']} not in registry")
                errors += 1

            try:
                jsonschema.validate(instance=r, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                print(f"Schema ERROR in rivalry {r['rivalry_id']}: {e.message}")
                errors += 1
                
        if errors > 0:
            print(f"Total schema/registry mapping errors: {errors}")
            sys.exit(1)
        else:
            print(f"Rivalries schema validation passed ({len(rivs)} rivalries).")

    print("ALL CHECKS PASSED.")
    sys.exit(0)

if __name__ == '__main__':
    run()
