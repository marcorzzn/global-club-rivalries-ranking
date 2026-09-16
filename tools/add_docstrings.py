import os

docstring = '''"""
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
'''

files = [
    'tools/validate.py',
    'tools/validate_dossier.py',
    'tools/integrate_dossiers.py',
    'tools/calculate_ncap.py',
    'tools/partial_ranking.py',
    'tools/partial_ranking_v2.py',
    'tools/map_flat_to_nested.py',
    'tools/extract_data.py',
    'tools/fetch_logos.py'
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if not content.startswith('"""\nMWI Framework'):
            with open(f, 'w', encoding='utf-8') as file:
                file.write(docstring + '\n' + content)
    except Exception as e:
        print(f'Error processing {f}: {e}')

print("Docstrings added successfully.")
