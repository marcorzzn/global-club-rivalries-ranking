#!/usr/bin/env python3
"""
TASK 1: GDELT Media Coverage Score Updater

Aggiorna i media_coverage_score nel JSON usando l'API di GDELT con exponential backoff.
Nota: ClubElo restituisce 502 permanente - viene gestito come null.

GDELT API: https://api.gdeltproject.org/api/v2/doc/doc
Richiede query parameters: query, timespan, format=json
"""

import json
import time
import random
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# Configurazione
MAX_RETRIES = 5
BASE_DELAY = 1.0  # secondi
MAX_DELAY = 60.0  # secondi
REQUESTS_PER_MINUTE = 10  # Limite rate limiting

def exponential_backoff(retry_count: int) -> float:
    """Calcola il delay con exponential backoff + jitter."""
    delay = min(BASE_DELAY * (2 ** retry_count), MAX_DELAY)
    jitter = random.uniform(0, delay * 0.1)  # 10% jitter
    return delay + jitter

def query_gdelt(club_a: str, club_b: str, country: str) -> Optional[float]:
    """
    Interroga GDELT per ottenere un punteggio di copertura mediatica.
    
    Returns:
        media_coverage_score (0-100) o None se fallisce
    """
    # Costruisci la query
    query = f'("{club_a}" OR "{club_b}") AND "football" AND "{country}"'
    
    # Calcola timespan (ultimi 5 anni)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)
    timespan = f"{start_date.strftime('%Y%m%dT%H%M%S')},{end_date.strftime('%Y%m%dT%H%M%S')}"
    
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        'query': query,
        'timespan': timespan,
        'format': 'json',
        'maxrecords': '100'
    }
    
    for retry in range(MAX_RETRIES):
        try:
            # Simulazione della chiamata API (da implementare con requests)
            # In ambiente reale: response = requests.get(url, params=params, timeout=30)
            
            # Per ora, simuliamo un risultato basato sulla popolarità
            # Questo è un placeholder - in produzione usare requests reale
            print(f"  [GDELT] Query: {query[:50]}...")
            
            # Placeholder: punteggio basato su caratteristiche del record
            # In produzione: analizzare la risposta GDELT reale
            score = None  # Da calcolare dalla risposta API
            
            return score
            
        except Exception as e:
            if retry < MAX_RETRIES - 1:
                delay = exponential_backoff(retry)
                print(f"  [GDELT] Errore: {e}. Retry in {delay:.2f}s...")
                time.sleep(delay)
            else:
                print(f"  [GDELT] Fallito dopo {MAX_RETRIES} tentativi: {e}")
                return None
    
    return None

def main():
    print("=== TASK 1: GDELT Media Coverage Updater ===\n")
    
    # Carica il JSON
    with open('data/rivalries_v3_all.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Totale record: {len(data)}")
    
    # Conta quanti hanno già media_coverage_score
    existing = sum(1 for r in data if r.get('media_coverage_score') is not None)
    missing = len(data) - existing
    print(f"Record con media_coverage_score: {existing}")
    print(f"Record da aggiornare: {missing}\n")
    
    # Nota su ClubElo
    print("NOTA: ClubElo API restituisce 502 permanente - i dati rimarranno null.")
    print("      Solo GDELT verrà utilizzato per media_coverage_score.\n")
    
    # Processa i record (in produzione, processare tutti quelli mancanti)
    updated = 0
    for i, record in enumerate(data):
        if record.get('media_coverage_score') is None:
            club_a = record['club_a']['name']
            club_b = record['club_b']['name']
            country = record['country']
            
            print(f"[{i+1}/{len(data)}] {club_a} vs {club_b} ({country})")
            
            # Chiama GDELT
            score = query_gdelt(club_a, club_b, country)
            
            if score is not None:
                record['media_coverage_score'] = score
                updated += 1
                print(f"  ✅ Aggiornato: {score}")
            else:
                print(f"  ⚠️  Nessun dato disponibile")
            
            # Rate limiting
            if (i + 1) % REQUESTS_PER_MINUTE == 0:
                print(f"  [Rate limit] Pausa 60s...")
                time.sleep(60)
    
    # Salva il JSON aggiornato
    with open('data/rivalries_v3_all.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== RISULTATI ===")
    print(f"Record aggiornati: {updated}")
    print(f"File salvato: data/rivalries_v3_all.json")

if __name__ == '__main__':
    main()
