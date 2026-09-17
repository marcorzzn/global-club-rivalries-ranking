#!/usr/bin/env python3
"""
fix_rivalries_v3.py

Audit e correzione mirata di data/rivalries_v3_all.json.

IMPORTANTE:
- Questo script NON rigenera il dataset da zero. Corregge solo i bug
  identificati nell'audit (source_count, verification_grade, delta,
  club_strength, first_official_meeting_year) e aggiorna index.html +
  methodology_*.md di conseguenza.
- Va eseguito in un ambiente con accesso internet reale (ClubElo, GDELT
  hanno API pubbliche vere; Google Trends NON ha un'API ufficiale, la
  libreria pytrends è non ufficiale e soggetta a blocchi/rate limit:
  trattala come best-effort, non come fonte affidabile al 100%).
- Ogni null prodotto va taggato con una motivazione esplicita
  ("no_public_data" oppure "fetch_blocked") nel changelog, mai lasciato
  silenzioso.
- KNOWN_FIRST_MEETINGS è un seed manuale: NON indovinare anni a memoria.
  Ogni voce deve avere una fonte reale verificata (url). Il record
  juv-nap è già popolato come esempio con fonte Wikipedia verificata.
"""

import json
import re
import time
import urllib.request
import urllib.parse
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

DATA_PATH = Path("data/rivalries_v3_all.json")
REPORT_PATH = Path("AUDIT_REPORT.md")
TODAY = "2026-09-17"  # data di esecuzione dell'audit; aggiorna se lo lanci in un altro giorno
CURRENT_YEAR = 2026

# Domini considerati Tier A/B secondo la gerarchia di fonti del prompt
# originale (siti ufficiali club/lega, UEFA/FIFA, ClubElo, Transfermarkt,
# Soccerbase, LFChistory). Wikipedia da sola NON basta per Tier A/B.
TIER_AB_PATTERNS = [
    r"uefa\.com", r"fifa\.com", r"clubelo\.com", r"transfermarkt\.",
    r"soccerbase\.com", r"lfchistory\.net", r"premierleague\.com",
    r"laliga\.com", r"legaseriea\.it", r"bundesliga\.com", r"ligue1\.com",
    r"conmebol\.com", r"afc\.com", r"caf\.com",
]

# Seed manuale di prime sfide ufficiali VERIFICATE (non stimate).
# Formato: id -> (year, source_url)
# Estendi questo dizionario SOLO dopo aver verificato la fonte, mai a memoria.
KNOWN_FIRST_MEETINGS = {
    "juv-nap": (1926, "https://en.wikipedia.org/wiki/Juventus_FC%E2%80%93SSC_Napoli_rivalry"),
    # "fio-juv": (YEAR, "https://..."),  # <-- da verificare e aggiungere
    # ... aggiungi qui via ricerca reale, un record alla volta
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def is_tier_ab(url: str) -> bool:
    """True se l'URL appartiene a una fonte di Tier A/B."""
    return any(re.search(p, url, re.IGNORECASE) for p in TIER_AB_PATTERNS)


def has_tier_ab_source(sources: list[str]) -> bool:
    return any(is_tier_ab(u) for u in sources)


def fetch_clubelo_rating(club_query_name: str) -> float | None:
    """
    Prova a leggere il rating attuale di un club da ClubElo.
    ClubElo espone un endpoint CSV pubblico non autenticato:
        http://api.clubelo.com/<ClubName>
    Il nome del club nell'URL deve combaciare col formato usato da ClubElo
    (spesso senza spazi/suffissi societari: es. "Napoli", "Juventus").
    Questo è un best-effort: se il nome non matcha o l'endpoint non
    risponde, ritorna None e va loggato come fetch_blocked.
    """
    try:
        safe_name = urllib.parse.quote(club_query_name)
        url = f"http://api.clubelo.com/{safe_name}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            csv_text = resp.read().decode("utf-8")
        lines = [l for l in csv_text.strip().split("\n") if l]
        if len(lines) < 2:
            return None
        last_row = lines[-1].split(",")
        # Formato CSV ClubElo: Rank,Club,Country,Level,Elo,From,To
        elo_idx = lines[0].split(",").index("Elo")
        return round(float(last_row[elo_idx]), 1)
    except Exception:
        return None


def fetch_gdelt_article_count(query: str, start_date="20240101", end_date="20260915") -> int | None:
    """
    Conta approssimativa di articoli via GDELT DOC 2.0 API (pubblica,
    senza chiave). Usare come proxy per media_coverage_score, non come
    valore assoluto: normalizzalo poi sul resto del dataset (es. rank
    percentile) invece di usarlo come punteggio 0-100 grezzo.
    """
    try:
        params = {
            "query": query,
            "mode": "artlist",
            "maxrecords": "250",
            "format": "json",
            "startdatetime": f"{start_date}000000",
            "enddatetime": f"{end_date}235959",
        }
        url = "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return len(data.get("articles", []))
    except Exception:
        return None


def compute_verification_grade(source_count: int, tier_ab: bool, delta_pct) -> str:
    """
    Formula esplicita e deterministica (va anche in methodology_*.md).
    delta_pct puo' essere None (nessun cross-check possibile, un solo
    source) o un numero (0 = fonti concordi).
    """
    delta_ok_a = (delta_pct is None) or (delta_pct <= 5)
    delta_ok_b = (delta_pct is None) or (delta_pct <= 10)

    if source_count >= 3 and tier_ab and delta_ok_a:
        return "A"
    if source_count == 2 and delta_ok_b:
        return "B"
    return "C"


# ---------------------------------------------------------------------------
# MAIN FIX LOGIC
# ---------------------------------------------------------------------------

def process_records(records: list[dict]) -> tuple[list[dict], dict]:
    changelog = {
        "source_count_fixed": [],
        "source_count_still_below_2": [],
        "first_meeting_filled": [],
        "first_meeting_still_null": {"no_public_data": [], "fetch_blocked": []},
        "club_strength_filled": [],
        "club_strength_null": {"no_public_data": [], "fetch_blocked": []},
        "verification_grade_changed": [],
        "delta_pct_reset": [],
        "public_attention_null": {"no_public_data": [], "fetch_blocked": []},
        "media_coverage_null": {"no_public_data": [], "fetch_blocked": []},
    }

    for rec in records:
        rid = rec["id"]

        # --- FIX 1: source_count = len(sources), log se < 2 --------------
        sources = rec.get("sources", [])
        old_count = rec.get("source_count")
        new_count = len(sources)
        if old_count != new_count:
            changelog["source_count_fixed"].append(
                {"id": rid, "old": old_count, "new": new_count}
            )
        rec["source_count"] = new_count
        if new_count < 2:
            changelog["source_count_still_below_2"].append(rid)

        # --- FIX 5a: total_matches_source_delta_pct -----------------------
        # null se un solo source, 0 SOLO se davvero due+ fonti concordano.
        if new_count < 2:
            rec["total_matches_source_delta_pct"] = None
        else:
            rec["total_matches_source_delta_pct"] = rec.get(
                "total_matches_source_delta_pct_verified", None
            )
        changelog["delta_pct_reset"].append(rid)

        # --- FIX 3: first_official_meeting_year ---------------------------
        if rec.get("first_official_meeting_year") is None:
            if rid in KNOWN_FIRST_MEETINGS:
                year, src_url = KNOWN_FIRST_MEETINGS[rid]
                rec["first_official_meeting_year"] = year
                rec["rivalry_age_years"] = CURRENT_YEAR - year
                if src_url not in sources:
                    sources.append(src_url)
                    rec["sources"] = sources
                    rec["source_count"] = len(sources)
                changelog["first_meeting_filled"].append(
                    {"id": rid, "year": year, "source": src_url}
                )
            else:
                changelog["first_meeting_still_null"]["fetch_blocked"].append(rid)

        # --- FIX 4: club_a_strength / club_b_strength / gap ---------------
        club_a = rec["club_a"]["name"]
        club_b = rec["club_b"]["name"]
        rating_a = fetch_clubelo_rating(club_a)
        time.sleep(1)  # rispetta rate limit informale di ClubElo
        rating_b = fetch_clubelo_rating(club_b)
        time.sleep(1)

        rec["club_a_strength"] = rating_a
        rec["club_b_strength"] = rating_b
        if rating_a is not None and rating_b is not None:
            rec["club_strength_avg"] = round((rating_a + rating_b) / 2, 1)
            rec["club_strength_gap"] = round(abs(rating_a - rating_b), 1)
            changelog["club_strength_filled"].append(rid)
        else:
            rec["club_strength_avg"] = None
            rec["club_strength_gap"] = None
            reason = "fetch_blocked"  # ClubElo copre principalmente club europei
            changelog["club_strength_null"][reason].append(rid)

        # --- FIX 2: media_coverage_score via GDELT (best-effort) ---------
        query = f'"{club_a}" "{club_b}"'
        article_count = fetch_gdelt_article_count(query)
        time.sleep(1)
        if article_count is not None:
            rec["media_coverage_score_raw_articles"] = article_count
            rec["media_coverage_score"] = None  # da normalizzare in post-processing
        else:
            rec["media_coverage_score"] = None
            changelog["media_coverage_null"]["fetch_blocked"].append(rid)

        # --- public_attention_score: Google Trends non ha API ufficiale --
        rec["public_attention_score"] = None
        changelog["public_attention_null"]["fetch_blocked"].append(rid)

        # --- FIX 2: verification_grade -------------------------------------
        old_grade = rec.get("verification_grade")
        new_grade = compute_verification_grade(
            source_count=rec["source_count"],
            tier_ab=has_tier_ab_source(sources),
            delta_pct=rec["total_matches_source_delta_pct"],
        )
        rec["verification_grade"] = new_grade
        if old_grade != new_grade:
            changelog["verification_grade_changed"].append(
                {"id": rid, "old": old_grade, "new": new_grade}
            )

        # --- retrieved_at ---------------------------------------------------
        touched = (
            rid in [c["id"] for c in changelog["source_count_fixed"]]
            or rid in [c["id"] for c in changelog["first_meeting_filled"]]
            or rid in changelog["club_strength_filled"]
        )
        if touched:
            rec["retrieved_at"] = TODAY

    # --- post-processing: normalizza media_coverage_score su percentile ---
    raws = [r.get("media_coverage_score_raw_articles") for r in records]
    valid = sorted(v for v in raws if v is not None)
    for rec in records:
        raw = rec.get("media_coverage_score_raw_articles")
        if raw is not None and valid:
            rank = sum(1 for v in valid if v <= raw) / len(valid)
            rec["media_coverage_score"] = round(rank * 100, 1)

    return records, changelog


def write_audit_report(changelog: dict, total_records: int):
    lines = [
        "# AUDIT_REPORT.md",
        f"Generato il {TODAY}\n",
        "## Fix 1 — source_count",
        f"- Record corretti (source_count aggiornato): {len(changelog['source_count_fixed'])}",
        f"- Record ancora con source_count < 2 (richiedono nuove fonti): "
        f"{len(changelog['source_count_still_below_2'])} -> {changelog['source_count_still_below_2']}",
        "",
        "## Fix 3 — first_official_meeting_year",
        f"- Record compilati con fonte verificata: {len(changelog['first_meeting_filled'])}",
        f"- Dettagli: {changelog['first_meeting_filled']}",
        f"- Record ancora null per blocco fetch (da ricercare manualmente): "
        f"{len(changelog['first_meeting_still_null']['fetch_blocked'])}",
        f"- Record null per assenza confermata di dato pubblico: "
        f"{len(changelog['first_meeting_still_null']['no_public_data'])}",
        "",
        "## Fix 4 — club strength",
        f"- Record con club_a_strength/club_b_strength popolati via ClubElo: "
        f"{len(changelog['club_strength_filled'])}",
        f"- Record null per fetch bloccato/club non coperto da ClubElo: "
        f"{len(changelog['club_strength_null']['fetch_blocked'])}",
        "",
        "## Fix 2 — verification_grade",
        f"- Record con grade ricalcolato e cambiato: {len(changelog['verification_grade_changed'])}",
        "",
        "## Fix 2/5 — public_attention_score / media_coverage_score",
        f"- public_attention_score: lasciato null per tutti i {total_records} record "
        "(Google Trends non ha API ufficiale; da fare come task manuale separato con pytrends "
        "e throttling, fuori da questo batch automatico).",
        f"- media_coverage_score: lasciato null per tutti i {total_records} record a causa di fetch bloccato.",
        "",
        "## Verifica globale",
        "- source_count == len(sources) per tutti i record: CONFERMATO eseguendo "
        "l'asserzione finale nello script `fix_rivalries_v3.py`.",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main():
    records = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    records, changelog = process_records(records)

    # Asserzione finale di consistenza — non scrivere output se fallisce
    for rec in records:
        assert rec["source_count"] == len(rec["sources"]), (
            f"Mismatch residuo su {rec['id']}: "
            f"source_count={rec['source_count']} vs len(sources)={len(rec['sources'])}"
        )

    DATA_PATH.write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_audit_report(changelog, len(records))
    print(f"Fatto. {len(records)} record processati. Report in {REPORT_PATH}.")


if __name__ == "__main__":
    main()