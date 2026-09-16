import json
import os

with open('data/priority_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)
    
with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)
    
rivs_dict = {r['rivalry_id']: r for r in rivs}

# BACKFILL A (1-30) - match_context
batch_a1 = queue[0:15]
batch_a2 = queue[15:30]

for idx, b in enumerate([batch_a1, batch_a2]):
    out = []
    for r in b:
        rid = r['rivalry_id']
        tot = rivs_dict.get(rid, {}).get('h2h', {}).get('total', {}).get('value', 'unknown') if isinstance(rivs_dict.get(rid, {}).get('h2h', {}).get('total'), dict) else rivs_dict.get(rid, {}).get('h2h', {}).get('total', 'unknown')
        
        out.append({
            'rivalry_id': rid,
            'total_matches_to_split': tot,
            'match_context': {'continental_finals': None, 'top5_league': None, 'top10_league': None, 'national_cups': None, 'state_regional': None}
        })
    with open(f'dossiers/backfill_a{idx+1}_template.json', 'w') as f:
        json.dump(out, f, indent=2)
    
    prompt = '''Compila SOLO il campo `match_context` per queste 15 rivalità.
Per ogni rivalità, suddividi il totale nei 5 livelli competitivi:
- continental_finals: match in finali di coppe continentali
- top5_league: match in campionati top 5 europei
- top10_league: match in campionati top 10 (Brasileirão, Liga MX, ecc.)
- national_cups: match in coppe nazionali
- state_regional: match in campionati statali/regionali

Rispondi SOLO con un JSON array identico al template fornito. Zero amichevoli.
RIVALITA:\n'''
    for r in b: prompt += f"- {r['rivalry_id']}\n"
    with open(f'dossiers/backfill_a{idx+1}_prompt.txt', 'w', encoding='utf-8') as f: f.write(prompt)

# BACKFILL B (31-50) - semantic metrics
batch_b1 = queue[30:40]
batch_b2 = queue[40:50]

for idx, b in enumerate([batch_b1, batch_b2]):
    out = []
    for r in b:
        out.append({
            'rivalry_id': r['rivalry_id'],
            'h_dom': {'value': None, 'source': '...'},
            'h_cont': {'value': None, 'source': '...'},
            'h_club': {'value': None, 'source': '...'},
            'i_soc': {'value': None, 'source': '...'},
            'i_name': {'value': None, 'source': '...'},
            'stadium': {'a': {'value': None, 'source': '...'}, 'b': {'value': None, 'source': '...'}},
            'attendance': {'value': None, 'source': '...'}
        })
    with open(f'dossiers/backfill_b{idx+1}_template.json', 'w') as f:
        json.dump(out, f, indent=2)
        
    prompt = '''Compila SOLO le metriche semantiche per queste 10 rivalità.
Campi da compilare:
- h_dom (0-100): finali di coppa nazionale / spareggi-scudetto documentati
- h_cont (0-100): stadio massimo raggiunto in coppe continentali
- h_club (0-100): trofei combinati 1976-2026
- i_soc (0-100): frattura sociale/politica documentata
- i_name (0-100): nome storico documentato
- stadium.a e stadium.b: capienza ufficiale
- attendance: affluenza media

Rispondi SOLO con un JSON array identico al template fornito.
RIVALITA:\n'''
    for r in b: prompt += f"- {r['rivalry_id']}\n"
    with open(f'dossiers/backfill_b{idx+1}_prompt.txt', 'w', encoding='utf-8') as f: f.write(prompt)
