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
import glob
import os
import csv

def run():
    print("Integrating validated dossiers into registry...")
    
    with open('data/rivalries.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)
        
    registry_map = {r['rivalry_id']: r for r in registry}
    integration_report = []
    
    batch_files = glob.glob('dossiers/batch_*_completed.json')
    if not batch_files:
        print("No completed dossiers found.")
        return
        
    for bf in batch_files:
        with open(bf, 'r', encoding='utf-8') as f:
            dossiers = json.load(f)
            
        for d in dossiers:
            rid = d['rivalry_id']
            if rid not in registry_map:
                integration_report.append({'rivalry_id': rid, 'status': 'REJECTED', 'reason': 'Unknown ID'})
                continue
                
            target = registry_map[rid]
            
            # Helper to map fields cleanly
            def merge_metric(t, s, keys):
                for k in keys:
                    if k in s and s[k].get('value') is not None:
                        if k not in t: t[k] = {}
                        t[k]['value'] = s[k]['value']
                        t[k]['source'] = s[k]['source']
                        t[k]['retrieved_at'] = s[k].get('retrieved_at', '2026-09-17')
            
            # Map H2H
            h2h = d.get('h2h', {})
            if h2h.get('total', {}).get('value') is not None:
                target['h2h']['total'] = h2h['total']['value']
                target['h2h']['w_a'] = h2h.get('w_a', {}).get('value')
                target['h2h']['d'] = h2h.get('d', {}).get('value')
                target['h2h']['w_b'] = h2h.get('w_b', {}).get('value')
                target['h2h']['active_decades'] = h2h.get('active_decades', {}).get('value')
                target['h2h']['source'] = h2h['total'].get('source')
                target['h2h']['retrieved_at'] = h2h['total'].get('retrieved_at', '2026-09-17')
                
            merge_metric(target, d, ['h_dom', 'h_cont', 'i_soc', 'i_name', 'attendance'])
            
# Map match_context
            if 'match_context' in d:
                if 'match_context' not in target:
                    target['match_context'] = {}
                merge_metric(target['match_context'], d['match_context'], ['continental_finals', 'top5_league', 'top10_league', 'national_cups', 'state_regional'])
            
            # Map stadium
            if 'stadium' in d:
                if d['stadium'].get('a', {}).get('value'):
                    target['stadium']['a'] = d['stadium']['a']['value']
                    target['stadium']['source'] = d['stadium']['a']['source']
                    target['stadium']['retrieved_at'] = d['stadium']['a'].get('retrieved_at')
                if d['stadium'].get('b', {}).get('value'):
                    target['stadium']['b'] = d['stadium']['b']['value']
                    
            integration_report.append({'rivalry_id': rid, 'status': 'INTEGRATED', 'reason': 'Success'})

    with open('data/rivalries.json', 'w', encoding='utf-8') as f:
        json.dump(list(registry_map.values()), f, indent=2)
        
    with open('integration_report.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['rivalry_id', 'status', 'reason'])
        w.writeheader()
        w.writerows(integration_report)
        
    print(f"Integrated {len(integration_report)} dossiers. See integration_report.csv")

if __name__ == '__main__':
    run()
