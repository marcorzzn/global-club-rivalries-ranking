"""
scripts/merge_logos.py
Inietta i loghi da data/logos.json in rivalries_ranking.json e
rivalries_encyclopaedia.json come campi logo1 / logo2.

Regole:
- Il match avviene per nome squadra esatto (case-sensitive come in logos.json)
- Se il logo non è in logos.json → logo1/logo2 = null (ESPLICITO, non omesso)
- Non viene inventato nessun URL; i null sono visibili nell'output JSON

Idempotente: può essere rieseguito dopo ogni fetch_logos.py senza effetti collaterali.
"""
import json
import os


def load_logos() -> dict:
    path = 'data/logos.json'
    if not os.path.exists(path):
        print(f"[ERRORE] {path} non trovato. Esegui prima fetch_logos.py")
        return {}
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def inject_logos(rivalries: list, logos: dict) -> tuple[list, int, int]:
    """
    Aggiunge logo1/logo2 a ogni voce.
    Restituisce (rivalries_aggiornate, n_trovati, n_mancanti).
    """
    found = 0
    missing = 0
    for r in rivalries:
        l1 = logos.get(r.get('team1', ''))
        l2 = logos.get(r.get('team2', ''))
        r['logo1'] = l1   # None se non trovato — intenzionale
        r['logo2'] = l2
        if l1:
            found += 1
        else:
            missing += 1
        if l2:
            found += 1
        else:
            missing += 1
    return rivalries, found, missing


def process_file(path: str, logos: dict):
    if not os.path.exists(path):
        print(f"[SKIP] {path} non trovato")
        return
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    updated, found, missing = inject_logos(data, logos)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(updated, f, ensure_ascii=False, indent=2)
    total_slots = found + missing
    print(f"  {path}: {found}/{total_slots} loghi trovati ({missing} null espliciti)")


def main():
    logos = load_logos()
    if not logos:
        return
    print(f"Loghi in logos.json: {len(logos)}")
    process_file('data/rivalries_ranking.json', logos)
    process_file('data/rivalries_encyclopaedia.json', logos)
    print("✓ Merge completato.")


if __name__ == "__main__":
    main()
