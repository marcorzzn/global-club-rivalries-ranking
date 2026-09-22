"""
scripts/clean_ranking.py
Rimuove dal ranking le voci con p_raw chiaramente errato
(identificato dall'audit: fonte W+D+L su sottotabelle o numeri di giocatore).

Criteri di esclusione applicati:
  - Derby della Madonnina: W+D+L 31+17+3=51 (sottotabella, reale >200)
  - Derby d'Italia: W+D+L 6+15+25=46 (sottotabella, reale >230)
  - Paulista Derby: "unbeaten in 25 games" (striscia di un giocatore, non totale match)
  - Avellaneda Derby: "714 games for the club" (presenze di Bochini, non scontri diretti)
  - Uruguayan Clasico: W+D+L 25+9+7=41 (sottotabella, reale >1000)

Mantenute:
  - Osaka Derby (75 da W+D+L): plausibile per J1 League 1982-2026 (~1.7/anno)
  - Hudson River Derby (46 da W+D+L): plausibile per MLS 2015-2026 (~4/anno)

Ogni esclusione aggiornata in ranking_excluded.json con motivazione esplicita.
"""
import json

FALSE_POSITIVES = {
    "derby_della_madonnina": "W+D+L 31+17+3=51: subset table (Champions League/European only), real total >200",
    "derby_d_italia":        "W+D+L 6+15+25=46: subset table, real total >230",
    "paulista_derby":        "Text match 'unbeaten in 25 games': a player streak, not total meetings",
    "avellaneda_derby":      "Text match '714 games for the club': Bochini individual appearances, not head-to-head total",
    "uruguayan_clasico":     "W+D+L 25+9+7=41: subset table, real total >1000 (Nacional vs Penarol since 1900)",
}

with open('data/rivalries_ranking.json', encoding='utf-8') as f:
    ranking = json.load(f)

with open('data/ranking_excluded.json', encoding='utf-8') as f:
    excluded = json.load(f)

kept = []
newly_excluded = []

for r in ranking:
    if r['id'] in FALSE_POSITIVES:
        reason = f"FALSE POSITIVE detected by audit: {FALSE_POSITIVES[r['id']]}"
        print(f"  REMOVING {r['name_en']}: {reason}")
        newly_excluded.append({
            "title": r['wikipedia_url'].split('/wiki/')[-1],
            "id": r['id'],
            "reason": reason,
            "p_raw_extracted": r['p_raw'],
            "p_raw_source_detail": r.get('p_raw_source_detail', '')
        })
    else:
        kept.append(r)

excluded.extend(newly_excluded)

with open('data/rivalries_ranking.json', 'w', encoding='utf-8') as f:
    json.dump(kept, f, ensure_ascii=False, indent=2)
with open('data/ranking_excluded.json', 'w', encoding='utf-8') as f:
    json.dump(excluded, f, ensure_ascii=False, indent=2)

print(f"\nRanking pulito: {len(kept)} voci")
print(f"Totale escluse (log trasparente): {len(excluded)}")
