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
import math

with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)

with open('data/ncap_config.json', 'r', encoding='utf-8') as f:
    ncap_config = json.load(f)
ncap = ncap_config['ncap']

print(f'Partial Ranking (Batch 1-3) - N_cap: {ncap}:')
results = []
for r in rivs:
    h2h = r.get('h2h', {})
    total = h2h.get('total')
    if total is None:
        continue
        
    w_a = h2h.get('w_a')
    d = h2h.get('d')
    w_b = h2h.get('w_b')
    active_decades = h2h.get('active_decades') or 5
    
    # R: using dynamic ncap
    r_vol = 100 * min(total, ncap) / ncap
    r_cont = 100 * active_decades / 5
    r_score = 0.60 * r_vol + 0.40 * r_cont
    
    # H
    h_dom = r.get('h_dom', {}).get('value') or 0
    h_cont = r.get('h_cont', {}).get('value') or 0
    h_club = r.get('h_club', {}).get('value') or 0
    h_score = 0.40 * h_dom + 0.35 * h_cont + 0.25 * h_club
    
    # I
    i_soc = r.get('i_soc', {}).get('value') or 0
    i_name = r.get('i_name', {}).get('value') or 0
    
    pa = w_a / total if total > 0 else 0
    pd = d / total if total > 0 else 0
    pb = w_b / total if total > 0 else 0
    
    ent = 0
    for p in [pa, pd, pb]:
        if p > 0:
            ent -= p * math.log(p)
            
    i_bal = (100 * ent / math.log(3))
    i_score = 0.50 * i_bal + 0.25 * i_name + 0.25 * i_soc
    
    # S
    sa = r.get('stadium', {}).get('a') or 0
    sb = r.get('stadium', {}).get('b') or 0
    att = r.get('attendance', {}).get('value') or 0
    cap_mean = (sa + sb) / 2
    s_cap = 100 * min(cap_mean, 80000) / 80000
    s_att = 100 * min(att, 70000) / 70000
    s_score = 0.50 * s_cap + 0.50 * s_att
    
    mwi = (28 * r_score + 44 * i_score + 18 * h_score + 10 * s_score) / 100
    
    results.append({'id': r['rivalry_id'], 'mwi': round(mwi, 1), 'r': round(r_score,1), 'h': round(h_score,1), 'i': round(i_score,1), 's': round(s_score,1)})
    
results.sort(key=lambda x: x['mwi'], reverse=True)
for i, res in enumerate(results):
    print(f"{i+1}. {res['id']} - MWI: {res['mwi']} (R:{res['r']}, I:{res['i']}, H:{res['h']}, S:{res['s']})")
