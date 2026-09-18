#!/usr/bin/env python3
"""
TASK 3: Standardizzazione ID nel JSON
Converte ID puramente numerici (es. "071") in formato slug (es. "caf-001")
basato sulla confederazione di appartenenza.

Mapping:
- CAF → caf-XXX
- AFC → afc-XXX
- CONMEBOL → con-XXX
- CONCACAF → nac-XXX
- OFC → ofc-XXX
- UEFA → uefa-XXX (se necessario)
"""

import json
from typing import Dict, Any

CONFEDERATION_PREFIX = {
    'CAF': 'caf',
    'AFC': 'afc',
    'CONMEBOL': 'con',
    'CONCACAF': 'nac',
    'OFC': 'ofc',
    'UEFA': 'uefa'
}

def normalize_id(old_id: str, confederation: str) -> str:
    """Converte un ID numerico in formato slug."""
    if not old_id.isdigit():
        return old_id  # Già in formato corretto
    
    prefix = CONFEDERATION_PREFIX.get(confederation, 'unk')
    new_id = f"{prefix}-{int(old_id):03d}"
    return new_id

def main():
    # Carica il JSON
    with open('data/rivalries_v3_all.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Totale record: {len(data)}")
    
    # Identifica record con ID numerici
    numeric_records = [r for r in data if r['id'].isdigit()]
    print(f"Record con ID numerici: {len(numeric_records)}")
    
    # Crea mapping vecchio→nuovo ID
    id_mapping: Dict[str, str] = {}
    for record in numeric_records:
        old_id = record['id']
        new_id = normalize_id(old_id, record['confederation'])
        id_mapping[old_id] = new_id
        print(f"  {old_id} → {new_id} ({record['confederation']})")
    
    if not id_mapping:
        print("Nessun ID da convertire.")
        return
    
    # Applica le conversioni
    updated_count = 0
    for record in data:
        if record['id'] in id_mapping:
            old_id = record['id']
            record['id'] = id_mapping[old_id]
            updated_count += 1
    
    # Salva il JSON aggiornato
    with open('data/rivalries_v3_all.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{updated_count} ID aggiornati con successo.")
    print("File salvato: data/rivalries_v3_all.json")

if __name__ == '__main__':
    main()
