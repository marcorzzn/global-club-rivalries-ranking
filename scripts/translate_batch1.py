"""
scripts/translate_batch1.py  — v2
Batch 1 traduzioni IT — rivalità già presenti nel ranking.

METODO CORRETTO (v2):
  Usa action=query&prop=langlinks&lllang=it — restituisce il titolo ESATTO
  della pagina italiana ufficialmente collegata, senza ambiguità di nome.
  
  Poi usa quel titolo per chiamare l'API REST IT e ottenere il summary.

MOTIVO del cambio:
  v1 cercava "titolo_EN" su it.wikipedia.org direttamente — fallisce quando
  il titolo italiano è diverso (es. "Superclásico" → "Derby di Buenos Aires",
  "Old Firm" → invariato ma potrebbe non trovare redirect).
  
  v2 parte dall'articolo EN e chiede: "esiste una versione italiana? qual è
  il suo titolo esatto?" — zero falsi negativi per differenza di titolo.
"""
import json
import os
import sys
import time

import requests

HEADERS = {
    'User-Agent': 'RivalitaDataCollector/2.0 '
                  '(https://github.com/marcorzzn/global-club-rivalries-ranking)'
}
API_EN  = "https://en.wikipedia.org/w/api.php"
REST_IT = "https://it.wikipedia.org/api/rest_v1/page/summary/{}"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import make_id


def get_it_title_via_langlinks(title_en: str) -> str | None:
    """
    Usa l'API langlinks di Wikipedia EN per trovare il titolo esatto
    della pagina italiana collegata ufficialmente.
    Restituisce il titolo IT o None se non esiste una versione italiana.
    """
    params = {
        "action":  "query",
        "titles":  title_en,
        "prop":    "langlinks",
        "lllang":  "it",
        "format":  "json",
        "redirects": 1,
    }
    try:
        r = requests.get(API_EN, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            for ll in page.get("langlinks", []):
                if ll.get("lang") == "it":
                    return ll.get("*")  # titolo esatto IT
    except Exception as e:
        print(f"  [langlinks err] {e}")
    return None


def get_it_summary(it_title: str) -> str:
    """Fetcha il summary della pagina italiana dato il suo titolo esatto."""
    url = REST_IT.format(requests.utils.quote(it_title.replace(' ', '_'), safe=''))
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return r.json().get('extract', '')
    except Exception:
        pass
    return ''


def main():
    with open('data/rivalries_ranking.json', encoding='utf-8') as f:
        ranking = json.load(f)

    with open('data/rivalries_encyclopaedia.json', encoding='utf-8') as f:
        enc = json.load(f)

    enc_by_id = {e['id']: i for i, e in enumerate(enc)}

    print(f"Rivalità nel ranking: {len(ranking)}")
    print(f"Voci enciclopedia:    {len(enc)}")
    print()

    updated   = 0
    already_ok = 0
    no_it_page = 0
    not_in_enc = 0

    for rank_entry in ranking:
        rid = rank_entry['id']
        wiki_title = rank_entry['wikipedia_url'].split('/wiki/')[-1].replace('_', ' ')
        print(f"[{rid}] — EN title: '{wiki_title}'")

        # Trova nell'enciclopedia
        idx = enc_by_id.get(rid)
        if idx is None:
            wiki_id = make_id(wiki_title)
            idx = enc_by_id.get(wiki_id)
        if idx is None:
            print(f"  -> NON nell'enciclopedia")
            not_in_enc += 1
            time.sleep(0.2)
            continue

        entry = enc[idx]

        # Già tradotta bene?
        if entry.get('summary_it') and len(entry.get('summary_it', '')) > 100:
            print(f"  -> Gia' tradotta ({len(entry['summary_it'])} chars)")
            already_ok += 1
            continue

        # Cerca pagina IT tramite langlinks ufficiali
        it_title = get_it_title_via_langlinks(wiki_title)
        time.sleep(0.4)

        if not it_title:
            print(f"  -> Nessuna versione italiana ufficiale su Wikipedia")
            no_it_page += 1
            enc[idx]['summary_it'] = ''
            continue

        # Fetch summary IT
        it_summary = get_it_summary(it_title)
        time.sleep(0.3)

        if it_summary:
            enc[idx]['summary_it'] = it_summary
            enc[idx]['name_it']    = it_title
            print(f"  -> IT trovata: '{it_title}' ({len(it_summary)} chars)")
            updated += 1
        else:
            enc[idx]['summary_it'] = ''
            print(f"  -> Pagina IT '{it_title}' esiste ma summary vuoto")
            no_it_page += 1

    with open('data/rivalries_encyclopaedia.json', 'w', encoding='utf-8') as f:
        json.dump(enc, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*40}")
    print(f"Aggiornate:                  {updated}")
    print(f"Gia' OK (>100 chars):        {already_ok}")
    print(f"Senza pagina IT ufficiale:   {no_it_page}")
    print(f"Non nell'enciclopedia:       {not_in_enc}")


if __name__ == "__main__":
    main()
