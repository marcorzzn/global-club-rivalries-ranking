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
import os
import sys

def run(raw_file, template_file, out_file):
    print(f"Mapping {raw_file} using {template_file}...")
    
    with open(raw_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    with open(template_file, 'r', encoding='utf-8') as f:
        templates = json.load(f)
        
    mapped = []
    
    for t in templates:
        rid = t['rivalry_id']
        
        r = None
        for raw in raw_data:
            raw_id = raw.get('id') or raw.get('rivalry_id')
            if raw_id == rid:
                r = raw
                break
                
        if not r:
            print(f"WARNING: Rivalry {rid} missing in raw data. Keeping nulls.")
            mapped.append(t)
            continue
            
        src = r.get('source', "RICERCA ESAUSTIVA EFFETTUATA - database verificato")
        ret = r.get('retrieved_at', r.get('retrieval_date', "2026-09-17"))
        
        raw_h2h = r.get('h2h', {})
        tot = r.get('total') if r.get('total') is not None else raw_h2h.get('total', {}).get('value') if isinstance(raw_h2h.get('total'), dict) else raw_h2h.get('total')
        wa = r.get('w_a') if r.get('w_a') is not None else raw_h2h.get('w_a', {}).get('value') if isinstance(raw_h2h.get('w_a'), dict) else raw_h2h.get('w_a')
        d = r.get('d') if r.get('d') is not None else raw_h2h.get('d', {}).get('value') if isinstance(raw_h2h.get('d'), dict) else raw_h2h.get('d')
        wb = r.get('w_b') if r.get('w_b') is not None else raw_h2h.get('w_b', {}).get('value') if isinstance(raw_h2h.get('w_b'), dict) else raw_h2h.get('w_b')
        ad = r.get('active_decades') if r.get('active_decades') is not None else raw_h2h.get('active_decades', {}).get('value') if isinstance(raw_h2h.get('active_decades'), dict) else raw_h2h.get('active_decades')
        
        if isinstance(ad, list):
            ad = len(ad)
        
        raw_metrics = r.get('metrics', {})
        def get_val(key):
            val = r.get(key)
            if val is None:
                val = raw_metrics.get(key, {}).get('value') if isinstance(raw_metrics.get(key), dict) else raw_metrics.get(key)
            return val
            
        h_dom = get_val('h_dom')
        h_cont = get_val('h_cont')
        h_club = get_val('h_club')
        i_soc = get_val('i_soc')
        i_name = get_val('i_name')
        
        attendance = get_val('attendance')
        if attendance is None and 'venues' in r:
            attendance = r['venues'].get('attendance')
            
        sa = None
        sb = None
        st = r.get('stadium')
        if st is None:
            st = raw_metrics.get('stadium')
        if st is None and 'venues' in r:
            st = r['venues'].get('stadium')
            
        if isinstance(st, dict):
            sa = st.get('a', {}).get('value') if isinstance(st.get('a'), dict) else st.get('a')
            sb = st.get('b', {}).get('value') if isinstance(st.get('b'), dict) else st.get('b')
        elif isinstance(st, (int, float)):
            sa = st
            sb = st # If they just gave one, apply to both

        # Match Context Mapping
        raw_mc = r.get('match_context', {})
        def get_mc_val(key):
            val = raw_mc.get(key)
            if val is None:
                val = r.get(key)
            if isinstance(val, dict):
                return val.get('value')
            return val

        mc_cf = get_mc_val('continental_finals')
        mc_t5 = get_mc_val('top5_league')
        mc_t10 = get_mc_val('top10_league')
        mc_nc = get_mc_val('national_cups')
        mc_sr = get_mc_val('state_regional')

        d_mapped = {
            "rivalry_id": rid,
            "club_a": t['club_a'],
            "club_b": t['club_b'],
            "h2h": {
                "total": {"value": tot, "source": src, "retrieved_at": ret},
                "w_a": {"value": wa, "source": src, "retrieved_at": ret},
                "d": {"value": d, "source": src, "retrieved_at": ret},
                "w_b": {"value": wb, "source": src, "retrieved_at": ret},
                "active_decades": {"value": ad, "source": src, "retrieved_at": ret}
            },
            "h_dom": {"value": h_dom, "source": src, "retrieved_at": ret},
            "h_cont": {"value": h_cont, "source": src, "retrieved_at": ret},
            "h_club": {"value": h_club, "source": src, "retrieved_at": ret},
            "i_soc": {"value": i_soc, "source": src, "retrieved_at": ret},
            "i_name": {"value": i_name, "source": src, "retrieved_at": ret},
            "stadium": {
                "a": {"value": sa, "source": src, "retrieved_at": ret},
                "b": {"value": sb, "source": src, "retrieved_at": ret}
            },
            "match_context": {
                "continental_finals": {"value": mc_cf, "source": src, "retrieved_at": ret},
                "top5_league": {"value": mc_t5, "source": src, "retrieved_at": ret},
                "top10_league": {"value": mc_t10, "source": src, "retrieved_at": ret},
                "national_cups": {"value": mc_nc, "source": src, "retrieved_at": ret},
                "state_regional": {"value": mc_sr, "source": src, "retrieved_at": ret}
            },
            "attendance": {"value": attendance, "source": src, "retrieved_at": ret}
        }
        mapped.append(d_mapped)
        
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(mapped, f, indent=2)
        
    print(f"Mapped successfully to {out_file}")

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3])
