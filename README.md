# MWI Framework: Global Club Football Rivalry Index

## TL;DR
A composite index methodology for ranking football rivalries,
released as a reusable Python framework. The algorithm works;
automated data extraction does not (see Case Study below).

## What's Inside
- `tools/` — Complete pipeline: validators, scoring engines (V1 and V2), integrators
- `data/rivalries_verified_template.json` — Empty template for manual data entry
- `methodology_en.md` / `methodology_it.md` — Algorithm documentation
- `walkthrough.md` — Project narrative including the LLM audit

## Case Study: LLMs Cannot Do Historical Research (Yet)
During development, we built a rigorous pipeline and fed it
data extracted by LLM subagents. An independent manual audit
of 12 rivalries revealed:
- 75% of extracted data was wrong (30% to 1500% error)
- The LLM produced "mimetic coherence": plausible-looking
  numbers that satisfied mathematical constraints (w_a + d + w_b = total)
  but were fabricated
- Pattern: round numbers for obscure rivalries (150-100-100)

**Takeaway**: LLMs can structure research, not perform it.
Historical data must come from verified primary sources,
not model outputs validated only for structural coherence.

## Running the Algorithm
1. Fill `data/rivalries_verified_template.json` with your own verified data
2. `python tools/partial_ranking_v2.py`
3. View results in `rankings.json`

## Algorithm V2: Context-Aware Scoring
Corrects the volume bias that plagued V1 by weighting matches:
- Continental finals: 1.5x
- Top-5 leagues: 1.3x  
- Top-10 leagues: 1.2x
- National cups: 1.1x
- State/regional: 0.7x

Final weights: R=22%, I=40%, H=28%, S=10%
