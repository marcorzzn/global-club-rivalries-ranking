#!/usr/bin/env python3
"""
TASK 4: search_years.py - Estrazione first_official_meeting_year da Wikipedia

Script per estrarre l'anno del primo incontro ufficiale tra due club di calcio
usando le API di Wikipedia.

REGOLE RIGOROSE:
1. Solo incontri COMPETITIVI/UFFICIALI (League, Cup, competizioni UEFA/FIFA)
2. ESCLUDERE esplicitamente: amichevoli ("friendly"), esibizioni, coppe non ufficiali
3. Attenzione ai predecessori senza lignaggio esplicito
4. Non confondere anno fondazione con anno primo match

SISTEMA A FLAG:
- Se nel testo "prose" della pagina Wikipedia è menzionato un anno precedente
  a quello trovato in tabelle/infobox, aggiungere:
  [FLAG: EARLIER PROSE MENTION FOUND: XXXX]

WORKFLOW BATCH:
- Processa 20 record per volta
- Batch 1: record 0-19 (primi 20 con null)
- Output: candidates_report_batch.txt
- STOP per approvazione umana prima di scrivere nel JSON
"""

import json
import time
import random
import re
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
import requests

# Configurazione
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
REQUEST_DELAY = 1.0  # secondi tra le richieste
MAX_RETRIES = 5
BATCH_SIZE = 20
BATCH_START_INDEX = 0  # Inizia dal primo record con null
BATCH_END_INDEX = 20    # Fino al record 20

def exponential_backoff(retry_count: int) -> float:
    """Calcola il delay con exponential backoff + jitter."""
    base_delay = 2.0
    max_delay = 60.0
    delay = min(base_delay * (2 ** retry_count), max_delay)
    jitter = random.uniform(0, delay * 0.1)  # 10% jitter
    return delay + jitter

def make_wiki_request(params: Dict[str, Any], retry: int = 0) -> Optional[Dict]:
    """
    Effettua una richiesta alle API di Wikipedia con retry e delay.
    
    Returns:
        JSON response o None se fallisce
    """
    headers = {
        'User-Agent': 'FootballRivalryIndex/1.0 (https://github.com/example/rivalry-index; contact@example.com)',
        'Accept-Encoding': 'gzip',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(WIKIPEDIA_API_URL, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:  # Rate limited
            delay = exponential_backoff(retry)
            print(f"    [WIKI] Rate limited. Retry in {delay:.2f}s...")
            time.sleep(delay)
            if retry < MAX_RETRIES:
                return make_wiki_request(params, retry + 1)
        elif response.status_code == 403:
            print(f"    [WIKI] HTTP 403 Forbidden - User-Agent richiesto")
            return None
        else:
            print(f"    [WIKI] HTTP {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        if retry < MAX_RETRIES:
            delay = exponential_backoff(retry)
            print(f"    [WIKI] Errore: {e}. Retry in {delay:.2f}s...")
            time.sleep(delay)
            return make_wiki_request(params, retry + 1)
        else:
            print(f"    [WIKI] Fallito dopo {MAX_RETRIES} tentativi: {e}")
            return None
    
    return None

def get_page_content(title: str) -> Optional[str]:
    """Ottiene il contenuto testuale completo di una pagina Wikipedia."""
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'extracts',
        'explaintext': True,
        'redirects': 1
    }
    
    result = make_wiki_request(params)
    if result and 'query' in result and 'pages' in result['query']:
        pages = result['query']['pages']
        for page_id, page_data in pages.items():
            if page_id != '-1' and 'extract' in page_data:
                return page_data['extract']
    return None

def extract_first_meeting_year(text: str, club_a: str, club_b: str) -> Optional[Tuple[int, str, Optional[int]]]:
    """
    Estrae l'anno del primo incontro ufficiale dal testo di Wikipedia.
    
    Returns:
        Tuple di (anno, snippet_testo, earlier_prose_year) o None
    """
    if not text:
        return None
    
    # Pattern per anni (1800-2099)
    year_pattern = r'\b((?:18|19|20)\d{2})\b'
    
    # Parole chiave per incontri ufficiali
    official_keywords = [
        'first meeting', 'first match', 'first game', 'first played',
        'met for the first time', 'inaugural match', 'first competitive',
        'first league', 'first cup', 'first official', 'first encounter',
        'first fixture', 'first ever match', 'first history',
        'prima partita', 'primo incontro', 'first derby',
        'erste begegnung', 'premier match', 'primer partido'
    ]
    
    # Contesti ufficiali specifici
    official_contexts = [
        'league', 'cup', 'fa cup', 'championship', 'premier league',
        'serie a', 'la liga', 'bundesliga', 'ligue 1',
        'uefa', 'champions league', 'europa league',
        'copa del rey', 'dfb-pokal', 'coupe de france',
        'official competition', 'competitive match'
    ]
    
    # Parole da escludere (amichevoli, non ufficiali)
    exclude_keywords = [
        'friendly', 'exhibition', 'test match', 'benefit match',
        'charity match', 'testimonial', 'pre-season', 'warm-up',
        'practice match', 'scrimmage', 'unofficial'
    ]
    
    lines = text.split('\n')
    candidate_year = None
    candidate_snippet = None
    candidate_line_idx = -1
    all_mentions = []  # Tutti gli anni menzionati con contesto
    
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        
        # Salta linee troppo corte
        if len(line) < 20:
            continue
        
        # Salta linee con parole da escludere
        if any(kw in line_lower for kw in exclude_keywords):
            continue
        
        # Controlla se la linea menziona entrambi i club
        mentions_both = club_a.lower() in line_lower or club_b.lower() in line_lower
        
        # Cerca pattern di primo incontro
        is_first_mention = any(kw in line_lower for kw in official_keywords)
        
        if is_first_mention or mentions_both:
            years_in_line = re.findall(year_pattern, line)
            for year_str in years_in_line:
                year = int(year_str)
                
                # Ignora anni di fondazione (tipicamente molto vecchi)
                if year < 1850:
                    continue
                
                # Verifica se c'è contesto ufficiale
                has_official_context = any(ctx in line_lower for ctx in official_contexts)
                
                all_mentions.append({
                    'year': year,
                    'line': line.strip(),
                    'idx': idx,
                    'is_first': is_first_mention,
                    'has_official': has_official_context
                })
                
                # Preferisci incontri esplicitamente descritti come "first"
                if is_first_mention and has_official_context:
                    if candidate_year is None or year < candidate_year:
                        candidate_year = year
                        candidate_snippet = line.strip()[:300]
                        candidate_line_idx = idx
    
    # Se non troviamo con contesto ufficiale, prendi il primo "first meeting"
    if candidate_year is None:
        for mention in all_mentions:
            if mention['is_first']:
                candidate_year = mention['year']
                candidate_snippet = mention['line'][:300]
                candidate_line_idx = mention['idx']
                break
    
    # Se ancora nulla, cerca il primo anno dove si menzionano entrambi i club
    if candidate_year is None:
        for mention in all_mentions:
            if mention['has_official']:
                candidate_year = mention['year']
                candidate_snippet = mention['line'][:300]
                candidate_line_idx = mention['idx']
                break
    
    # Sistema a FLAG: cerca menzioni precedenti nel testo prose
    earlier_prose_year = None
    if candidate_year:
        for mention in all_mentions:
            if mention['year'] < candidate_year and not mention['is_first']:
                # Verifica se è una menzione valida (non fondatazione)
                if 'founded' not in mention['line'].lower() and 'established' not in mention['line'].lower():
                    earlier_prose_year = mention['year']
                    break
    
    if candidate_year:
        return (candidate_year, candidate_snippet or "", earlier_prose_year)
    
    return None

def search_rivalry_year(club_a: str, club_b: str, country: str, sources: List[str]) -> Optional[Dict]:
    """
    Cerca l'anno del primo incontro per una rivalità usando Wikipedia.
    
    Returns:
        Dict con {year, source_url, snippet, earlier_prose_year} o None
    """
    print(f"  🔍 Ricerca: {club_a} vs {club_b} ({country})")
    
    # Strategia 1: Cerca pagine di rivalità dirette
    rivalry_queries = [
        f"{club_a} vs {club_b} rivalry",
        f"{club_a}–{club_b} rivalry", 
        f"{club_a} {club_b} rivalry history",
        f"{club_a} against {club_b} first match"
    ]
    
    for query in rivalry_queries:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': 5
        }
        
        result = make_wiki_request(params)
        if result and 'query' in result and 'search' in result['query']:
            for item in result['query']['search']:
                title = item['title']
                
                # Ottieni il contenuto completo della pagina
                content = get_page_content(title)
                if content:
                    year_result = extract_first_meeting_year(content, club_a, club_b)
                    if year_result:
                        year, text_snippet, earlier_year = year_result
                        has_flag = earlier_year is not None
                        return {
                            'year': year,
                            'source_url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                            'snippet': text_snippet[:300],
                            'flag': has_flag,
                            'earlier_year': earlier_year
                        }
    
    # Strategia 2: Cerca pagine dedicate al derby (es. "Manchester Derby", "El Clásico")
    derby_terms = ['derby', 'clásico', 'clasico', 'derbi']
    for term in derby_terms:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': f"{club_a} {club_b} {term}",
            'srlimit': 3
        }
        
        result = make_wiki_request(params)
        if result and 'query' in result and 'search' in result['query']:
            for item in result['query']['search']:
                title = item['title']
                content = get_page_content(title)
                if content:
                    year_result = extract_first_meeting_year(content, club_a, club_b)
                    if year_result:
                        year, text_snippet, earlier_year = year_result
                        has_flag = earlier_year is not None
                        return {
                            'year': year,
                            'source_url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                            'snippet': text_snippet[:300],
                            'flag': has_flag,
                            'earlier_year': earlier_year
                        }
    
    # Strategia 3: Cerca nelle pagine dei singoli club (History section)
    for club in [club_a, club_b]:
        params = {
            'action': 'query',
            'format': 'json',
            'titles': club,
            'prop': 'extracts',
            'explaintext': True,
            'exsectionlimit': 5000,
            'redirects': 1
        }
        
        result = make_wiki_request(params)
        if result and 'query' in result and 'pages' in result['query']:
            pages = result['query']['pages']
            for page_id, page_data in pages.items():
                if page_id != '-1' and 'extract' in page_data:
                    extract = page_data['extract']
                    year_result = extract_first_meeting_year(extract, club_a, club_b)
                    if year_result:
                        year, text_snippet, earlier_year = year_result
                        has_flag = earlier_year is not None
                        return {
                            'year': year,
                            'source_url': f"https://en.wikipedia.org/wiki/{page_data['title'].replace(' ', '_')}",
                            'snippet': text_snippet[:300],
                            'flag': has_flag,
                            'earlier_year': earlier_year
                        }
    
    return None

def main():
    print("=" * 70)
    print("TASK 4: search_years.py - Estrazione first_official_meeting_year")
    print("=" * 70)
    print(f"\nData: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Batch: Record {BATCH_START_INDEX + 1} - {BATCH_END_INDEX}")
    print(f"Dimensione batch: {BATCH_SIZE} record\n")
    
    # Carica il JSON
    with open('data/rivalries_v3_all.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Identifica record con first_official_meeting_year = null
    null_records = [r for r in data if r.get('first_official_meeting_year') is None]
    
    print(f"Totale record con anno mancante: {len(null_records)}")
    print(f"Record da processare in questo batch: {min(BATCH_SIZE, len(null_records) - BATCH_START_INDEX)}\n")
    
    # Seleziona il batch corrente
    batch_records = null_records[BATCH_START_INDEX:BATCH_END_INDEX]
    
    if not batch_records:
        print("⚠️ Nessun record da processare in questo batch.")
        return
    
    results = []
    
    # Processa ogni record nel batch
    for i, record in enumerate(batch_records):
        print(f"\n[{i+1}/{len(batch_records)}] {record['id']}")
        
        club_a = record['club_a']['name']
        club_b = record['club_b']['name']
        country = record['country']
        sources = record.get('sources', [])
        
        # Cerca l'anno
        result = search_rivalry_year(club_a, club_b, country, sources)
        
        if result:
            flag_indicator = " ⚠️ FLAG" if result['flag'] else ""
            print(f"  ✅ Trovato: {result['year']}{flag_indicator}")
            print(f"     Fonte: {result['source_url'][:60]}...")
            
            results.append({
                'matchup': f"{club_a} vs {club_b}",
                'rivalry_name': record['rivalry_name'],
                'id': record['id'],
                'year': result['year'],
                'flag': result['flag'],
                'source_url': result['source_url'],
                'snippet': result['snippet']
            })
        else:
            print(f"  ❌ Nessun risultato trovato")
            results.append({
                'matchup': f"{club_a} vs {club_b}",
                'rivalry_name': record['rivalry_name'],
                'id': record['id'],
                'year': None,
                'flag': False,
                'source_url': 'N/A',
                'snippet': 'Nessun dato disponibile'
            })
    
    # Genera il report
    report_file = 'candidates_report_batch_11_30.txt'
    print(f"\n{'='*70}")
    print(f"Generazione report: {report_file}")
    print(f"{'='*70}\n")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("FOOTBALL RIVALRY INDEX - FIRST OFFICIAL MEETING YEAR CANDIDATES\n")
        f.write(f"Batch: Record {BATCH_START_INDEX + 1} - {BATCH_END_INDEX}\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Totale record processati: {len(results)}\n")
        f.write(f"Candidati trovati: {sum(1 for r in results if r['year'] is not None)}\n")
        f.write(f"Record con FLAG: {sum(1 for r in results if r['flag'])}\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("DETTAGLI CANDIDATI\n")
        f.write("=" * 70 + "\n\n")
        
        for i, r in enumerate(results, 1):
            f.write(f"{i}. MATCHUP: {r['matchup']}\n")
            f.write(f"   ID Record: {r['id']}\n")
            f.write(f"   Rivalry Name: {r['rivalry_name']}\n")
            f.write(f"   Anno Candidato: {r['year'] if r['year'] else 'NON TROVATO'}")
            if r['flag']:
                f.write(f" [FLAG: EARLIER PROSE MENTION FOUND]\n")
            else:
                f.write("\n")
            f.write(f"   Source URL: {r['source_url']}\n")
            f.write(f"   Snippet: \"{r['snippet']}\"\n")
            f.write("-" * 70 + "\n\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("ISTRUZIONI PER REVISIONE UMANA\n")
        f.write("=" * 70 + "\n\n")
        f.write("1. Verificare ogni candidato confrontando con la fonte URL\n")
        f.write("2. Per i record con FLAG, controllare se esiste un anno precedente valido\n")
        f.write("3. Confermare che si tratti di incontri COMPETITIVI/UFFICIALI\n")
        f.write("4. ESCLUDERE amichevoli, esibizioni, coppe non ufficiali\n")
        f.write("\nPer approvare e inserire nel JSON, eseguire:\n")
        f.write("  python3 apply_years.py --batch=1 --confirm\n\n")
        f.write("Per scartare tutti i risultati:\n")
        f.write("  python3 apply_years.py --batch=1 --discard\n")
    
    print(f"✅ Report generato: {report_file}")
    print(f"\n📋 RIEPILOGO:")
    print(f"   Record processati: {len(results)}")
    print(f"   Candidati validi: {sum(1 for r in results if r['year'] is not None)}")
    print(f"   Con flag da verificare: {sum(1 for r in results if r['flag'])}")
    
    print(f"\n⏸️  STOP - In attesa di approvazione umana")
    print(f"   Per favore, rivedi il file {report_file} e conferma prima di procedere.\n")

if __name__ == '__main__':
    main()
