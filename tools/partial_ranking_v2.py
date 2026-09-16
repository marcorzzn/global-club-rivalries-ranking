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

CONTEXT_WEIGHTS = {
    'continental_finals': 1.5,
    'top5_league': 1.3,
    'top10_league': 1.2,
    'national_cups': 1.1,
    'state_regional': 0.7
}

for r in rivs:
    mc = r.get('match_context', {})
    w_tot = 0
    for k in CONTEXT_WEIGHTS:
        val = mc.get(k, {}).get('value')
        if val:
            w_tot += CONTEXT_WEIGHTS[k] * val
    r['weighted_total'] = w_tot

# Calculate ncap_weighted
w_totals = [r['weighted_total'] for r in rivs if r['weighted_total'] > 0]
w_totals.sort()
if w_totals:
    idx = int(len(w_totals) * 0.95)
    ncap_weighted = w_totals[idx]
else:
    ncap_weighted = 250

print(f"N_cap Weighted: {ncap_weighted}")

scores = []
for r in rivs:
    if r.get('weighted_total', 0) == 0:
        continue
    
    h2h = r.get('h2h', {})
    def get_h2h(k, default=0):
        v = h2h.get(k)
        if isinstance(v, dict): return v.get('value', default)
        if isinstance(v, list): return len(v)
        return v if v is not None else default

    tot = get_h2h('total')
    wa = get_h2h('w_a')
    d = get_h2h('d')
    wb = get_h2h('w_b')
    ad = get_h2h('active_decades', 1)
    
    if tot == 0: continue
    
    pa, pd, pb = wa/tot, d/tot, wb/tot
    ent = 0
    k = 0
    for p in [pa, pd, pb]:
        if p > 0:
            ent -= p * math.log(p)
            k += 1
            
    i_bal = (100 * ent / math.log(3)) if k > 1 else 0
    
    r_vol_adj = 100 * min(r['weighted_total'], ncap_weighted) / ncap_weighted
    r_score = (r_vol_adj * 0.8) + (20 * (ad / 5.0))
    
    def get_val(key):
        val = r.get(key)
        if isinstance(val, dict): val = val.get('value')
        return float(val) if val is not None else 0.0
        
    h_dom = get_val('h_dom')
    h_cont = get_val('h_cont')
    h_club = get_val('h_club')
    i_soc = get_val('i_soc')
    i_name = get_val('i_name')
    
    att = get_val('attendance')
    st = r.get('stadium', {})
    
    st_a = st.get('a')
    if isinstance(st_a, dict): st_a = st_a.get('value')
    st_b = st.get('b')
    if isinstance(st_b, dict): st_b = st_b.get('value')
    
    st_a = st_a if st_a is not None else 0
    st_b = st_b if st_b is not None else 0
    cap_mean = (st_a + st_b) / 2
    
    i_score = (i_bal * 0.4) + (i_soc * 0.4) + (i_name * 0.2)
    h_score = (h_dom * 0.4) + (h_cont * 0.4) + (h_club * 0.2)
    s_score = 100 * min(att, cap_mean) / cap_mean if cap_mean > 0 else 0
    
    mwi = (22 * r_score + 40 * i_score + 28 * h_score + 10 * s_score) / 100
    
    scores.append({
        'id': r['rivalry_id'],
        'mwi': mwi,
        'r': r_score, 'i': i_score, 'h': h_score, 's': s_score
    })

scores.sort(key=lambda x: x['mwi'], reverse=True)

print(f"Partial Ranking V2 (N_cap_weighted: {ncap_weighted:.1f}):")
for i, s in enumerate(scores):
    print(f"{i+1}. {s['id']} - MWI: {s['mwi']:.1f} (R:{s['r']:.1f}, I:{s['i']:.1f}, H:{s['h']:.1f}, S:{s['s']:.1f})")
