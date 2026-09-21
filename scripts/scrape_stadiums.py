"""
scrape_stadiums.py
------------------
Uses the Wikidata SPARQL endpoint to collect stadium data for
football clubs, using paginated queries to avoid response size limits.

Outputs data/stadiums.json.
"""

import json
import re
import time
from pathlib import Path

import requests

BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_DIR  = BASE_DIR / "data"
INPUT     = DATA_DIR / "rivalries_encyclopaedia.json"
OUTPUT    = DATA_DIR / "stadiums.json"
DATA_DIR.mkdir(exist_ok=True)

SPARQL_URL = "https://query.wikidata.org/sparql"
DELAY      = 2.0   # seconds between SPARQL calls

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "RivalitaBot/1.0 (research project; rivalita@example.com)",
    "Accept":     "application/sparql-results+json",
})

# ---------------------------------------------------------------------------
# SPARQL query template – paginated with LIMIT / OFFSET
# We fetch clubs in batches of 500 to avoid huge response payloads
# ---------------------------------------------------------------------------

QUERY_PAGE = """
SELECT DISTINCT
  ?clubLabel
  ?stadiumLabel
  ?coords
  ?capacity
  ?cityLabel
  ?countryLabel
WHERE {{
  ?club wdt:P31 wd:Q476028 .
  ?club wdt:P115 ?stadium .
  OPTIONAL {{ ?stadium wdt:P625 ?coords . }}
  OPTIONAL {{ ?stadium wdt:P1083 ?capacity . }}
  OPTIONAL {{ ?stadium wdt:P131 ?city . }}
  OPTIONAL {{ ?club wdt:P17 ?country . }}
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "en" .
  }}
}}
LIMIT {limit}
OFFSET {offset}
"""

# Also a targeted query for a specific club name
QUERY_CLUB = """
SELECT DISTINCT
  ?clubLabel
  ?stadiumLabel
  ?coords
  ?capacity
  ?cityLabel
  ?countryLabel
WHERE {{
  ?club wdt:P31 wd:Q476028 .
  ?club rdfs:label "{name}"@en .
  ?club wdt:P115 ?stadium .
  OPTIONAL {{ ?stadium wdt:P625 ?coords . }}
  OPTIONAL {{ ?stadium wdt:P1083 ?capacity . }}
  OPTIONAL {{ ?stadium wdt:P131 ?city . }}
  OPTIONAL {{ ?club wdt:P17 ?country . }}
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "en" .
  }}
}}
LIMIT 3
"""


def run_sparql(query: str) -> list[dict]:
    try:
        r = SESSION.get(
            SPARQL_URL,
            params={"query": query, "format": "json"},
            timeout=90,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("results", {}).get("bindings", [])
    except Exception as e:
        print(f"  [WARN] SPARQL error: {e}")
        return []


def bv(b: dict, key: str) -> str:
    return b.get(key, {}).get("value", "")


def parse_coords(v: str) -> tuple:
    m = re.match(r"Point\(([0-9.\-]+)\s+([0-9.\-]+)\)", v or "")
    if m:
        return float(m.group(2)), float(m.group(1))   # lat, lng
    return None, None


def process_bindings(bindings: list[dict], seen: set) -> list[dict]:
    result = []
    for b in bindings:
        club    = bv(b, "clubLabel")
        stadium = bv(b, "stadiumLabel")
        if not club or not stadium:
            continue
        key = (club.lower(), stadium.lower())
        if key in seen:
            continue
        seen.add(key)
        lat, lng = parse_coords(bv(b, "coords"))
        cap_raw  = bv(b, "capacity")
        result.append({
            "club":     club,
            "stadium":  stadium,
            "lat":      lat,
            "lng":      lng,
            "capacity": int(float(cap_raw)) if cap_raw else None,
            "city":     bv(b, "cityLabel"),
            "country":  bv(b, "countryLabel"),
            "source":   "Wikidata SPARQL",
        })
    return result


def main():
    print("=" * 60)
    print("RIVALITA - Wikidata Stadium Scraper")
    print("=" * 60)

    seen     = set()
    stadiums = []

    # --- Step 1: Paginated bulk query
    PAGE_SIZE = 500
    MAX_PAGES = 12       # up to 6,000 clubs
    print(f"\n[1] Paginated Wikidata SPARQL (batch size={PAGE_SIZE}, max={MAX_PAGES} pages) ...")
    for page in range(MAX_PAGES):
        offset = page * PAGE_SIZE
        print(f"    Page {page+1}/{MAX_PAGES}  offset={offset} ...", end=" ", flush=True)
        q  = QUERY_PAGE.format(limit=PAGE_SIZE, offset=offset)
        bs = run_sparql(q)
        print(f"{len(bs)} bindings")
        batch = process_bindings(bs, seen)
        stadiums.extend(batch)
        if len(bs) < PAGE_SIZE:
            print("    (last page reached)")
            break
        time.sleep(DELAY)

    print(f"\n    Bulk result: {len(stadiums)} unique club/stadium pairs")

    # --- Step 2: Gap-fill from rivalry teams
    if INPUT.exists():
        print("\n[2] Loading rivalry teams to check coverage ...")
        rivalries  = json.loads(INPUT.read_text(encoding="utf-8"))
        team_names = set()
        for r in rivalries:
            if r.get("team1"):
                team_names.add(r["team1"])
            if r.get("team2"):
                team_names.add(r["team2"])

        existing_clubs = {s["club"].lower() for s in stadiums}
        missing        = [t for t in sorted(team_names) if t and t.lower() not in existing_clubs]
        print(f"    Rivalry teams missing from bulk result: {len(missing)}")

        for i, club in enumerate(missing[:150], 1):
            print(f"  [{i}/{min(len(missing),150)}] {club}")
            q     = QUERY_CLUB.format(name=club.replace('"', "'"))
            bs    = run_sparql(q)
            extra = process_bindings(bs, seen)
            stadiums.extend(extra)
            time.sleep(DELAY)
    else:
        print("\n[2] rivalries_encyclopaedia.json not found - skipping gap-fill.")

    # --- Step 3: Sort and save
    stadiums.sort(key=lambda x: x["club"])
    print(f"\n[3] Saving {len(stadiums)} records -> {OUTPUT}")
    OUTPUT.write_text(json.dumps(stadiums, ensure_ascii=False, indent=2), encoding="utf-8")
    print("    Done.")
    print(f"[OK] stadiums.json: {len(stadiums)} entries, {OUTPUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
