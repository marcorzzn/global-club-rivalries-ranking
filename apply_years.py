#!/usr/bin/env python3
"""
Script per applicare i first_official_meeting_year approvati al JSON.
Legge il report dei candidati e aggiorna il file rivalries_v3_all.json.

Uso:
  python apply_years.py --batch=1 --confirm   # Applica i dati del batch 1
  python apply_years.py --batch=1 --discard   # Scarta i dati del batch 1
  python apply_years.py --batch=2             # Processa batch 2 (record 21-40)
"""

import json
import argparse
import re
from typing import Dict, List, Optional
from datetime import datetime

JSON_FILE = "data/rivalries_v3_all.json"
REPORT_FILE = "candidates_report_batch_11_30.txt"

def parse_report(report_path: str) -> List[Dict]:
    """
    Parse il file report ed estrae i candidati approvati.
    
    Returns lista di dict con: id, year, source_url, snippet, has_flag
    """
    candidates = []
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern per estrarre ogni candidato
    pattern = r'''
        ^\d+\.\sMATCHUP:\s(?P<matchup>.+?)$\s*
        ^\s*ID\sRecord:\s(?P<id>\S+)\s*$\s*
        ^\s*Rivalry\sName:\s(?P<rivalry_name>.+?)$\s*
        ^\s*Anno\sCandidato:\s(?P<year>\d+)(?:\s*\[FLAG[^\]]*\])?\s*$\s*
        ^\s*Source\sURL:\s(?P<source_url>\S+)\s*$\s*
        ^\s*Snippet:\s"(?P<snippet>[^"]+)"
    '''
    
    matches = re.finditer(pattern, content, re.MULTILINE | re.VERBOSE)
    
    for match in matches:
        candidate = {
            'id': match.group('id'),
            'year': int(match.group('year')),
            'source_url': match.group('source_url'),
            'snippet': match.group('snippet')[:200],
            'has_flag': '[FLAG:' in content[match.start():match.end()]
        }
        candidates.append(candidate)
    
    return candidates


def load_json() -> List[Dict]:
    """Carica il file JSON delle rivalità."""
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: List[Dict]):
    """Salva il file JSON delle rivalità."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def apply_candidates(candidates: List[Dict], data: List[Dict]) -> Dict[str, any]:
    """
    Applica i candidati al dataset.
    
    Returns statistica degli aggiornamenti.
    """
    updated = 0
    skipped = 0
    not_found = 0
    
    # Crea mappa ID -> record
    id_to_record = {r['id']: r for r in data}
    
    for candidate in candidates:
        record_id = candidate['id']
        
        if record_id not in id_to_record:
            print(f"  ⚠️  ID non trovato: {record_id}")
            not_found += 1
            continue
        
        record = id_to_record[record_id]
        
        # Verifica che il campo sia null
        if record.get('first_official_meeting_year') is not None:
            print(f"  ⏭️  Saltato {record_id}: già ha anno {record['first_official_meeting_year']}")
            skipped += 1
            continue
        
        # Applica l'anno
        old_value = record.get('first_official_meeting_year')
        record['first_official_meeting_year'] = candidate['year']
        
        # Aggiungi la fonte se non esiste già
        if 'sources' in record:
            if candidate['source_url'] not in record['sources']:
                record['sources'].append(candidate['source_url'])
        
        # Aggiorna verification_grade se necessario
        # Se prima era null e ora abbiamo un anno verificato, migliora a B
        if record.get('verification_grade') == 'C':
            # Mantieni C se c'è un flag, altrimenti upgrade a B
            if not candidate['has_flag']:
                record['verification_grade'] = 'B'
        
        print(f"  ✅ {record_id}: {old_value} → {candidate['year']}")
        updated += 1
    
    return {
        'updated': updated,
        'skipped': skipped,
        'not_found': not_found
    }


def main():
    parser = argparse.ArgumentParser(description='Applica first_official_meeting_year al JSON')
    parser.add_argument('--batch', type=int, default=1, help='Numero del batch da applicare')
    parser.add_argument('--confirm', action='store_true', help='Conferma e applica le modifiche')
    parser.add_argument('--discard', action='store_true', help='Scarta i risultati del batch')
    
    args = parser.parse_args()
    
    if args.discard:
        print("❌ Risultati scartati. Nessuna modifica applicata.")
        return
    
    # Carica il report
    try:
        candidates = parse_report(REPORT_FILE)
    except FileNotFoundError:
        print(f"❌ Report non trovato: {REPORT_FILE}")
        return
    
    if not candidates:
        print("⚠️  Nessun candidato trovato nel report.")
        return
    
    print(f"📋 Batch {args.batch}: {len(candidates)} candidati trovati")
    
    if not args.confirm:
        print("\n⏸️  Modalità DRY-RUN (nessuna modifica sarà applicata)")
        print("    Usa --confirm per applicare le modifiche")
        print("    Usa --discard per scartare i risultati\n")
        
        # Mostra anteprima
        for i, c in enumerate(candidates[:5]):
            flag_str = " ⚠️ FLAG" if c['has_flag'] else ""
            print(f"  {i+1}. {c['id']}: {c['year']}{flag_str}")
        if len(candidates) > 5:
            print(f"  ... e altri {len(candidates) - 5} record")
        
        return
    
    # Carica il JSON
    print(f"\n📂 Caricamento {JSON_FILE}...")
    data = load_json()
    
    # Applica le modifiche
    print("🔄 Applicazione modifiche...\n")
    stats = apply_candidates(candidates, data)
    
    # Salva il JSON
    print(f"\n💾 Salvataggio {JSON_FILE}...")
    save_json(data)
    
    # Report finale
    print("\n" + "=" * 60)
    print("✅ APPLICAZIONE COMPLETATA")
    print("=" * 60)
    print(f"   Record aggiornati: {stats['updated']}")
    print(f"   Record saltati:    {stats['skipped']}")
    print(f"   ID non trovati:    {stats['not_found']}")
    print(f"   Totale processati: {len(candidates)}")
    
    # Conta quanti null rimangono
    null_count = sum(1 for r in data if r.get('first_official_meeting_year') is None)
    print(f"\n   📊 first_official_meeting_year null rimanenti: {null_count}")


if __name__ == '__main__':
    main()
