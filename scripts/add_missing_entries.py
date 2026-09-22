"""
scripts/add_missing_entries.py
Aggiunge manualmente le voci che la traversata Wikipedia non ha catturato
(non in nessuna sottocategoria raggiunta) e corregge id/nome di voci
presenti con titolo diverso.

Voci da aggiungere:
  - "North West derby (association football)" — Man Utd vs Liverpool
    Wikipedia lo classifica in categorie che lo scraper non ha raggiunto

  - "El Gran Derbi" — Sevilla vs Real Betis
    Stesso problema di categoria mancante

Correzione:
  - "Derby Paulista" (id=derby_paulista) → normalizza name_en e id
    perché il ranking usa id=paulista_derby (invertito)
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


def fetch_summary(title: str, lang: str = 'en') -> tuple[str, str]:
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title.replace(' ', '_'), safe='')}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            ts = datetime.now(timezone.utc).isoformat()
            return data.get('extract', ''), ts
    except Exception:
        pass
    return '', ''


SEEDS = [
    {
        "wikipedia_title": "North West derby (association football)",
        "name_en":    "North West Derby",
        "name_it":    "Derby del Nord-Ovest",
        "team1":      "Manchester United",
        "team2":      "Liverpool FC",
        "continent":  "Europe",
        "country":    "England",
        "type":       "regional",
    },
    {
        "wikipedia_title": "El Gran Derbi",
        "name_en":    "El Gran Derbi",
        "name_it":    "Il Gran Derbi",
        "team1":      "Sevilla FC",
        "team2":      "Real Betis",
        "continent":  "Europe",
        "country":    "Spain",
        "type":       "city_derby",
    },
]


def main():
    with open('data/rivalries_encyclopaedia.json', encoding='utf-8') as f:
        enc = json.load(f)

    ids_present = {e['id'] for e in enc}

    for seed in SEEDS:
        title = seed['wikipedia_title']
        new_id = make_id(seed['name_en'])

        if new_id in ids_present:
            print(f"[SKIP] {new_id} already present")
            continue

        print(f"[ADD] {title} -> id={new_id}")
        summary_en, ts = fetch_summary(title, 'en')
        time.sleep(0.4)
        summary_it, _  = fetch_summary(title, 'it')
        time.sleep(0.4)

        if not summary_en:
            print(f"  [WARN] No EN summary found, adding with empty summary")

        entry = {
            "id":            new_id,
            "name_en":       seed['name_en'],
            "name_it":       seed['name_it'],
            "team1":         seed.get('team1'),
            "team2":         seed.get('team2'),
            "continent":     seed['continent'],
            "country":       seed['country'],
            "league":        None,
            "type":          seed['type'],
            "wikipedia_url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            "summary_en":    summary_en,
            "summary_it":    summary_it,
            "source":        "Wikipedia (manual seed)",
            "data_retrieved": ts,
            "logo1":         None,
            "logo2":         None,
        }
        enc.append(entry)
        ids_present.add(new_id)
        print(f"  -> Added ({len(summary_en)} chars EN)")

    # Correggi "Derby Paulista" → assicura che abbia anche id=paulista_derby come alias
    # (la voce derby_paulista esiste già, il ranking usa paulista_derby)
    for entry in enc:
        if entry['id'] == 'derby_paulista':
            # Aggiunge un secondo entry con l'id corretto che il ranking usa
            corrected_id = 'paulista_derby'
            if corrected_id not in ids_present:
                print(f"\n[FIX] Adding paulista_derby alias for derby_paulista")
                alias = dict(entry)
                alias['id'] = corrected_id
                enc.append(alias)
                ids_present.add(corrected_id)

    with open('data/rivalries_encyclopaedia.json', 'w', encoding='utf-8') as f:
        json.dump(enc, f, ensure_ascii=False, indent=2)

    print(f"\nEnciclopedia aggiornata: {len(enc)} voci")


if __name__ == "__main__":
    main()
