"""
scripts/translate_batch1.py
Batch 1 traduzioni IT — rivalità già presenti nel ranking.

Strategia:
  1. Per ogni rivalità del ranking, cerca la pagina Wikipedia IT con lo stesso
     titolo o con il titolo EN, tramite API REST.
  2. Se trovata: usa il titolo IT come name_it, il summary IT come summary_it.
  3. Se non trovata: lascia name_it = name_en, summary_it = "" — MAI inventato.

Aggiorna rivalries_encyclopaedia.json solo per le voci il cui id corrisponde
a una rivalità del ranking (alta priorità).

NON modifica rivalries_ranking.json (i name_it sono già impostati a mano
con qualità accettabile per il ranking).
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests

HEADERS = {
    'User-Agent': 'RivalitaDataCollector/2.0 '
                  '(https://github.com/marcorzzn/global-club-rivalries-ranking)'
}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import make_id


def get_it_summary(title_en: str) -> tuple[str, str]:
    """
    Cerca su Wikipedia IT per titolo EN (spesso coincide o viene redirectato).
    Restituisce (it_title, it_summary) oppure ('', '').
    Timestamp NON necessario qui (è per data_retrieved del ranking).
    """
    url = f"https://it.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title_en.replace(' ', '_'), safe='')}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            return data.get('title', ''), data.get('extract', '')
    except Exception:
        pass
    return '', ''


def main():
    # Carica ranking per sapere quali id sono prioritari
    with open('data/rivalries_ranking.json', encoding='utf-8') as f:
        ranking = json.load(f)
    ranking_ids = {r['id']: r for r in ranking}

    # Carica enciclopedia
    with open('data/rivalries_encyclopaedia.json', encoding='utf-8') as f:
        enc = json.load(f)

    updated = 0
    already_ok = 0
    not_found = 0

    # Indice rapido per id
    enc_by_id = {e['id']: i for i, e in enumerate(enc)}

    print(f"Rivalità nel ranking: {len(ranking_ids)}")
    print(f"Voci enciclopedia: {len(enc)}")
    print()

    for rank_entry in ranking:
        rid = rank_entry['id']
        name_en = rank_entry['name_en']
        wiki_title = rank_entry['wikipedia_url'].split('/wiki/')[-1].replace('_', ' ')

        print(f"[{rid}]")

        # Trova la voce nell'enciclopedia
        idx = enc_by_id.get(rid)

        if idx is None:
            # Cerca per make_id del titolo wikipedia
            wiki_id = make_id(wiki_title)
            idx = enc_by_id.get(wiki_id)

        if idx is None:
            print(f"  -> Non trovata nell'enciclopedia (aggiungere manualmente se necessario)")
            not_found += 1
            # Comunque traduci il name_it nel ranking stesso
            time.sleep(0.3)
            continue

        entry = enc[idx]

        # Controlla se ha già summary IT
        if entry.get('summary_it') and len(entry.get('summary_it', '')) > 50:
            print(f"  -> Gia' tradotta ({len(entry['summary_it'])} chars)")
            already_ok += 1
            continue

        # Cerca su Wikipedia IT
        it_title, it_summary = get_it_summary(wiki_title)
        time.sleep(0.4)

        if it_summary:
            enc[idx]['summary_it'] = it_summary
            enc[idx]['name_it'] = it_title if it_title else entry.get('name_it', name_en)
            print(f"  -> IT trovata: '{it_title}' ({len(it_summary)} chars)")
            updated += 1
        else:
            enc[idx]['summary_it'] = ''
            print(f"  -> Nessuna pagina IT (lasciato vuoto)")
            not_found += 1

    # Salva
    with open('data/rivalries_encyclopaedia.json', 'w', encoding='utf-8') as f:
        json.dump(enc, f, ensure_ascii=False, indent=2)

    print(f"\nRiepilogo:")
    print(f"  Aggiornate: {updated}")
    print(f"  Gia' OK:    {already_ok}")
    print(f"  Non trovate su IT Wikipedia: {not_found}")


if __name__ == "__main__":
    main()
