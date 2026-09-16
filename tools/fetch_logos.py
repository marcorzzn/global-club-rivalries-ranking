import json
import os
import sys
import argparse
import requests
import time
import hashlib
from datetime import datetime

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Plan download only')
    parser.add_argument('--clean', action='store_true', help='Not used in this version directly for wipe, as shell does archive')
    args = parser.parse_args()

    with open('data/clubs.json', 'r', encoding='utf-8') as f:
        clubs = json.load(f)

    if args.dry_run:
        print(f"--- DRY RUN: Planning download for {len(clubs)} clubs ---")
        missing_count = 0
        for c in clubs:
            if not c.get('logo_url'):
                print(f"[{c['slug']}] MISSING URL")
                missing_count += 1
            else:
                print(f"[{c['slug']}] -> {c['logo_url']}")
        print(f"Total: {len(clubs)}, Missing URLs: {missing_count}")
        return

    # Real run
    os.makedirs('logos', exist_ok=True)
    manifest = []
    missing_logos = []
    
    headers = {'User-Agent': 'MWI-50-Ultra-Bot/1.0'}

    for c in clubs:
        slug = c['slug']
        url = c.get('logo_url')
        if not url:
            missing_logos.append({'slug': slug, 'official_name': c.get('official_name')})
            continue

        ext = url.split('.')[-1].lower()
        if ext not in ['png', 'svg', 'jpg', 'jpeg']:
            ext = 'png'
            
        filepath = f"logos/{slug}.{ext}"
        
        # Idempotent check
        if os.path.exists(filepath):
            file_hash = sha256_file(filepath)
            manifest.append({
                'slug': slug, 'file': f"{slug}.{ext}", 'source_url': url,
                'sha256': file_hash, 'license': c.get('logo_license'),
                'attribution': c.get('attribution'), 'fetched_at': datetime.utcnow().isoformat()
            })
            continue

        # Fetch
        success = False
        for attempt in range(3):
            try:
                print(f"Fetching {slug}...")
                r = requests.get(url, headers=headers, timeout=20)
                if r.status_code == 200:
                    with open(filepath, 'wb') as img:
                        img.write(r.content)
                    success = True
                    break
            except Exception as e:
                print(f"Attempt {attempt+1} failed for {slug}: {e}")
                time.sleep(2)
                
        if success:
            manifest.append({
                'slug': slug, 'file': f"{slug}.{ext}", 'source_url': url,
                'sha256': sha256_file(filepath), 'license': c.get('logo_license'),
                'attribution': c.get('attribution'), 'fetched_at': datetime.utcnow().isoformat()
            })
        else:
            missing_logos.append({'slug': slug, 'official_name': c.get('official_name')})

    with open('logos/manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    if missing_logos:
        import csv
        with open('missing_logos.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['slug', 'official_name'])
            writer.writeheader()
            writer.writerows(missing_logos)
        print(f"WARNING: {len(missing_logos)} logos missing. See missing_logos.csv")
        sys.exit(1)

    print("All logos fetched successfully.")
    sys.exit(0)

if __name__ == '__main__':
    run()
