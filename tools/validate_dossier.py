"""
MWI Framework - Rivalry Index Calculator
=========================================
A reusable framework for calculating composite rivalry indices
with context-aware weighting and entropy-based balance scoring.

USAGE:
    1. Popola data/rivalries_verified_template.json con dati verificati manualmente
    2. python tools/partial_ranking_v2.py
    3. Output: rankings.json + audit_report.csv

LICENSE: MIT
CASE STUDY: See walkthrough.md for the audit that exposed
           LLM hallucination risks in historical data extraction.
"""

import json
import jsonschema
import sys
import os

def run(batch_file):
    print(f"Validating dossier: {batch_file}...")
    
    with open(batch_file, 'r', encoding='utf-8') as f:
        dossiers = json.load(f)
        
    errors = []
    
    null_h2h_count = 0
    for d in dossiers:
        if d.get('h2h', {}).get('total', {}).get('value') is None:
            null_h2h_count += 1
            
    if null_h2h_count > 2:
        print(f"REJECTED: {null_h2h_count}/5 rivalità hanno H2H null")
        sys.exit(1)
    
    for d in dossiers:
        rid = d.get('rivalry_id')
        if not rid:
            errors.append({"rivalry_id": "UNKNOWN", "error": "Missing rivalry_id or structure modified"})
            continue
            
        try:
            h2h = d.get('h2h', {})
            t = h2h.get('total', {}).get('value')
            wa = h2h.get('w_a', {}).get('value')
            draw = h2h.get('d', {}).get('value')
            wb = h2h.get('w_b', {}).get('value')
            
            if t is not None and wa is not None and draw is not None and wb is not None:
                if t != (wa + draw + wb):
                    errors.append({
                        "rivalry_id": rid,
                        "error": f"H2H mismatch: {t} != {wa} + {draw} + {wb}"
                    })
                    
            att = d.get('attendance', {}).get('value')
            sa = d.get('stadium', {}).get('a', {}).get('value')
            if att and (not sa or att > sa * 1.5):
                errors.append({
                    "rivalry_id": rid,
                    "error": f"Attendance {att} seems anomalous compared to stadium A {sa}"
                })
                
        except Exception as e:
            errors.append({"rivalry_id": rid, "error": str(e)})

    if errors:
        print(f"Validation FAILED with {len(errors)} anomalies.")
        import csv
        with open('dossier_failures.csv', 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=['rivalry_id', 'error'])
            w.writeheader()
            w.writerows(errors)
        sys.exit(1)
    else:
        print("Dossier is structurally sound and arithmetically coherent. Ready for integration.")
        sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_dossier.py <path_to_batch.json>")
        sys.exit(1)
    run(sys.argv[1])
