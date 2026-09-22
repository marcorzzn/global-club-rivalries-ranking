"""
scripts/fix_remaining.py
Tre fix in un unico script:

1. Fetch summaries per North West Derby + El Gran Derbi (vuoti nel seed manuale)
   usando API extracts (non REST, che fallisce con parentesi nel titolo)

2. Aggiunge Derby di Torino all'enciclopedia (presente nel ranking, mancante nell'enc)

3. Rimuove logos.json corrente e lo ricostruisce da zero con piprop=thumbnail
   (fix SVG — eseguito dopo fix_logos.py che ha già il codice corretto)
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import make_id

HEADERS = {
    'User-Agent': 'RivalitaDataCollector/2.0 '
                  '(https://github.com/marcorzzn/global-club-rivalries-ranking)'
}
API_EN = "https://en.wikipedia.org/w/api.php"


def fetch_extract(title: str) -> tuple[str, str]:
    """Usa API extracts (più robusta del REST per titoli con parentesi)."""
    params = {
        "action": "query", "prop": "extracts",
        "exsentences": 8, "explaintext": 1,
        "titles": title, "format": "json", "redirects": 1,
    }
    try:
        r = requests.get(API_EN, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        ts = datetime.now(timezone.utc).isoformat()
        pages = r.json().get('query', {}).get('pages', {})
        for page in pages.values():
            return page.get('extract', ''), ts
    except Exception as e:
        print(f"  [extract err] {e}")
    return '', ''


def main():
    with open('data/rivalries_encyclopaedia.json', encoding='utf-8') as f:
        enc = json.load(f)

    enc_by_id = {e['id']: i for i, e in enumerate(enc)}

    # ── Fix 1: North West Derby summary ──
    nwd_id = make_id("North West Derby")
    if nwd_id in enc_by_id:
        idx = enc_by_id[nwd_id]
        if not enc[idx].get('summary_en'):
            print("[FIX] North West Derby: fetching summary...")
            summary, ts = fetch_extract("North West derby (association football)")
            enc[idx]['summary_en']    = summary
            enc[idx]['data_retrieved'] = ts
            print(f"  -> {len(summary)} chars")
            time.sleep(0.5)
            # IT via langlinks
            it_params = {
                "action": "query", "titles": "North West derby (association football)",
                "prop": "langlinks", "lllang": "it",
                "format": "json", "redirects": 1,
            }
            r = requests.get(API_EN, params=it_params, headers=HEADERS, timeout=15)
            pages = r.json().get('query', {}).get('pages', {})
            it_title = None
            for page in pages.values():
                for ll in page.get('langlinks', []):
                    if ll.get('lang') == 'it':
                        it_title = ll.get('*')
            if it_title:
                it_url = f"https://it.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(it_title.replace(' ', '_'), safe='')}"
                r2 = requests.get(it_url, headers=HEADERS, timeout=15)
                if r2.status_code == 200:
                    enc[idx]['summary_it'] = r2.json().get('extract', '')
                    enc[idx]['name_it']    = it_title
                    print(f"  -> IT: '{it_title}' ({len(enc[idx]['summary_it'])} chars)")
            time.sleep(0.5)
    else:
        print(f"[WARN] North West Derby not in encyclopaedia (id={nwd_id})")

    # ── Fix 2: El Gran Derbi summary ──
    egd_id = make_id("El Gran Derbi")
    if egd_id in enc_by_id:
        idx = enc_by_id[egd_id]
        if not enc[idx].get('summary_en'):
            print("[FIX] El Gran Derbi: fetching summary...")
            summary, ts = fetch_extract("El Gran Derbi")
            enc[idx]['summary_en']    = summary
            enc[idx]['data_retrieved'] = ts
            print(f"  -> {len(summary)} chars")
            time.sleep(0.5)
    else:
        print(f"[WARN] El Gran Derbi not in encyclopaedia (id={egd_id})")

    # ── Fix 3: Derby di Torino (nel ranking, non nell'enc) ──
    dt_id = make_id("Derby di Torino")
    if dt_id not in enc_by_id:
        print("[ADD] Derby di Torino: fetching and adding...")
        summary_en, ts = fetch_extract("Derby di Torino")
        time.sleep(0.4)
        # IT via langlinks
        it_params = {
            "action": "query", "titles": "Derby di Torino",
            "prop": "langlinks", "lllang": "it",
            "format": "json", "redirects": 1,
        }
        r = requests.get(API_EN, params=it_params, headers=HEADERS, timeout=15)
        pages = r.json().get('query', {}).get('pages', {})
        it_title = None
        summary_it = ''
        for page in pages.values():
            for ll in page.get('langlinks', []):
                if ll.get('lang') == 'it':
                    it_title = ll.get('*')
        if it_title:
            it_url = f"https://it.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(it_title.replace(' ', '_'), safe='')}"
            r2 = requests.get(it_url, headers=HEADERS, timeout=15)
            if r2.status_code == 200:
                summary_it = r2.json().get('extract', '')

        enc.append({
            "id":            dt_id,
            "name_en":       "Derby di Torino",
            "name_it":       it_title or "Derby di Torino",
            "team1":         "Juventus FC",
            "team2":         "Torino FC",
            "continent":     "Europe",
            "country":       "Italy",
            "league":        "Serie A",
            "type":          "city_derby",
            "wikipedia_url": "https://en.wikipedia.org/wiki/Derby_di_Torino",
            "summary_en":    summary_en,
            "summary_it":    summary_it,
            "source":        "Wikipedia (manual seed)",
            "data_retrieved": ts,
            "logo1":         None,
            "logo2":         None,
        })
        print(f"  -> Added ({len(summary_en)} chars EN)")

    with open('data/rivalries_encyclopaedia.json', 'w', encoding='utf-8') as f:
        json.dump(enc, f, ensure_ascii=False, indent=2)

    print(f"\nEnciclopedia: {len(enc)} voci")
    print("Fix completati.")


if __name__ == "__main__":
    main()
