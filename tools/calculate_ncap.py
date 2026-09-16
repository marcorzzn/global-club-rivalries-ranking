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

with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)

totals = []
for r in rivs:
    h2h = r.get('h2h', {})
    total = h2h.get('total')
    if isinstance(total, dict):
        total = total.get('value')
    if total is not None:
        totals.append(total)

if not totals:
    print("ERROR: no valid totals found")
    exit(1)

totals.sort()
# Calculate 95th percentile using pure Python (nearest rank)
idx = int(len(totals) * 0.95)
if idx >= len(totals):
    idx = len(totals) - 1
ncap = totals[idx]

print(f"Dataset size: {len(totals)} rivalries")
print(f"Total range: {min(totals)} - {max(totals)}")
print(f"95th percentile (N_cap): {ncap}")

with open('data/ncap_config.json', 'w') as f:
    json.dump({"ncap": ncap, "calculated_at": "2026-09-17", "dataset_size": len(totals)}, f, indent=2)
