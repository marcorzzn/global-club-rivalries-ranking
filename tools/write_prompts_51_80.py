import json
import os

with open('data/priority_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

base_prompt = '''Sei un ricercatore di dati storici calcistici per il progetto "Global Club Football Rivalry Index (MWI-50 Ultra, 1976-2026)".
Il tuo compito è completare un dossier JSON strutturato per 5 rivalità calcistiche mondiali.

## 1. REGOLA CRITICA SULLE AMICHEVOLI (pena rigetto batch)
- DIVIETO ASSOLUTO di includere match amichevoli nei totali H2H.
- Sono ammessi SOLO match ufficiali: campionato nazionale, coppe nazionali, coppe continentali.
- Sottrai le amichevoli se la tua fonte le include.

## 2. REGOLE STRUTTURALI E ARITMETICHE
- w_a + d + w_b == total deve valere per ogni rivalità.
- Rispondi ESATTAMENTE con un array JSON che segue il template fornito. MAI inventare valori: se non trovi, usa null. Fonte obbligatoria per ogni value non-null.

## 3. MATCH_CONTEXT
Aggiungi un oggetto `match_context` che scompone il totale H2H per livello competitivo:
- `continental_finals`: match in finali di coppe continentali
- `top5_league`: match in campionati top 5
- `top10_league`: match in campionati top 10 (es. Brasileirão, Liga MX, Primeira Liga)
- `national_cups`: match in coppe nazionali
- `state_regional`: match in campionati statali/regionali

## 4. METRICHE SEMANTICHE E STORICHE
- h_dom (0-100): finali di coppa nazionale / spareggi-scudetto documentati
- h_cont (0-100): stadio massimo raggiunto in coppe continentali
- h_club (0-100): trofei combinati 1976-2026
- i_soc (0-100): frattura sociale/politica documentata
- i_name (0-100): nome storico documentato
- stadium.a e stadium.b: capienza ufficiale
- attendance: affluenza media
- active_decades: (intero 1-5)

## RIVALITA:\n'''

os.makedirs('dossiers', exist_ok=True)

# Batches 10 to 15: 50:55, 55:60, 60:65, 65:70, 70:75, 75:80
for i in range(6):
    start = 50 + i * 5
    end = start + 5
    batch = queue[start:end]
    b_idx = i + 10
    
    prompt = base_prompt
    for r in batch: prompt += f"- {r['rivalry_id']}\n"
    
    with open(f'dossiers/batch_{b_idx:03d}_prompt.txt', 'w', encoding='utf-8') as f:
        f.write(prompt)
        
    out = []
    for r in batch:
        out.append({
            'rivalry_id': r['rivalry_id'],
            'club_a': r['club_a_slug'],
            'club_b': r['club_b_slug'],
            'h2h': {
                'total': {'value': None, 'source': '...'},
                'w_a': {'value': None, 'source': '...'},
                'd': {'value': None, 'source': '...'},
                'w_b': {'value': None, 'source': '...'},
                'active_decades': {'value': None, 'source': '...'}
            },
            'h_dom': {'value': None, 'source': '...'},
            'h_cont': {'value': None, 'source': '...'},
            'h_club': {'value': None, 'source': '...'},
            'i_soc': {'value': None, 'source': '...'},
            'i_name': {'value': None, 'source': '...'},
            'stadium': {'a': {'value': None, 'source': '...'}, 'b': {'value': None, 'source': '...'}},
            'attendance': {'value': None, 'source': '...'},
            'match_context': {
                'continental_finals': {'value': None, 'source': '...'},
                'top5_league': {'value': None, 'source': '...'},
                'top10_league': {'value': None, 'source': '...'},
                'national_cups': {'value': None, 'source': '...'},
                'state_regional': {'value': None, 'source': '...'}
            }
        })
    with open(f'dossiers/batch_{b_idx:03d}_template.json', 'w') as f:
        json.dump(out, f, indent=2)

print('Prompts and templates for 51-80 generated.')
