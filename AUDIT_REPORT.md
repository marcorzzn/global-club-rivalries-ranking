# AUDIT_REPORT.md
Generato il 2026-09-17

## Fix 1 — source_count
- Record corretti (source_count aggiornato): 100
- Record ancora con source_count < 2 (richiedono nuove fonti): 0 -> []

## Fix 3 — first_official_meeting_year
- Record compilati con fonte verificata: 1
- Dettagli: [{'id': 'juv-nap', 'year': 1926, 'source': 'https://en.wikipedia.org/wiki/Juventus_FC%E2%80%93SSC_Napoli_rivalry'}]
- Record ancora null per blocco fetch (da ricercare manualmente): 95
- Record null per assenza confermata di dato pubblico: 0

## Fix 4 — club strength
- Record con club_a_strength/club_b_strength popolati via ClubElo: 0
- Record null per fetch bloccato/club non coperto da ClubElo: 100

## Fix 2 — verification_grade
- Record con grade ricalcolato e cambiato: 1

## Fix 2/5 — public_attention_score / media_coverage_score
- public_attention_score: lasciato null per tutti i 100 record (Google Trends non ha API ufficiale; da fare come task manuale separato con pytrends e throttling, fuori da questo batch automatico).
- media_coverage_score: lasciato null per tutti i 100 record a causa di fetch bloccato.

## Verifica globale
- source_count == len(sources) per tutti i record: CONFERMATO eseguendo l'asserzione finale nello script `fix_rivalries_v3.py`.