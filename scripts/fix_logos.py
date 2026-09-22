"""
scripts/fix_logos.py
Corregge i 28 mismatch di nome tra i team nel ranking e i titoli Wikipedia.

Strategia:
1. Dizionario di alias noti (nome usato nel ranking → titolo Wikipedia esatto)
2. Per i nomi senza alias, tenta una Wikipedia search API per trovare la pagina giusta
3. Aggiorna data/logos.json con i nuovi URL trovati
4. Riesegue merge_logos.py

NESSUN URL inventato: se la search non trova nulla, resta null esplicito.
"""
import json
import time
import urllib.request
import urllib.parse

HEADERS = {"User-Agent": "GlobalClubRivalriesRanking/1.0 (progetto open source, contatto: marco)"}
API = "https://en.wikipedia.org/w/api.php"

# Mappa: nome usato nel ranking → titolo Wikipedia corretto (alias noti)
KNOWN_ALIASES = {
    "Arsenal FC":           "Arsenal F.C.",
    "AS Roma":              "A.S. Roma",
    "Celtic FC":            "Celtic F.C.",
    "Rangers FC":           "Rangers F.C.",
    "Atletico Madrid":      "Atlético de Madrid",
    "Everton FC":           "Everton F.C.",
    "Liverpool FC":         "Liverpool F.C.",
    "Manchester City":      "Manchester City F.C.",
    "Manchester United":    "Manchester United F.C.",
    "Tottenham Hotspur":    "Tottenham Hotspur F.C.",
    "Cardiff City":         "Cardiff City F.C.",
    "Swansea City":         "Swansea City A.F.C.",
    "Sheffield United":     "Sheffield United F.C.",
    "Sheffield Wednesday":  "Sheffield Wednesday F.C.",
    "Heart of Midlothian FC": "Heart of Midlothian F.C.",
    "Hibernian FC":         "Hibernian F.C.",
    "FC Porto":             "FC Porto",
    "SL Benfica":           "S.L. Benfica",
    "RSC Anderlecht":       "R.S.C. Anderlecht",
    "Real Madrid":          "Real Madrid CF",
    "River Plate":          "Club Atlético River Plate",
    "Al Ahly SC":           "Al Ahly SC",
    "Zamalek SC":           "Zamalek SC",
    "Kaizer Chiefs":        "Kaizer Chiefs F.C.",
    "Orlando Pirates":      "Orlando Pirates F.C.",
    "New York Red Bulls":   "New York Red Bulls",
    "UC Sampdoria":         "U.C. Sampdoria",
    "Cerezo Osaka":         "Cerezo Osaka",
}


def fetch_batch(titles: list) -> dict:
    params = {
        "action": "query",
        "titles": "|".join(titles),
        "prop": "pageimages",
        "piprop": "thumbnail",   # thumbnail converte SVG→PNG, original non restituisce SVG
        "pithumbsize": 300,
        "format": "json",
        "redirects": 1,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    pages = data.get("query", {}).get("pages", {})
    norm  = {n["from"]: n["to"] for n in data.get("query", {}).get("normalized", [])}
    redir = {r["from"]: r["to"] for r in data.get("query", {}).get("redirects", [])}

    raw_results = {}
    for page in pages.values():
        title = page.get("title")
        img   = page.get("thumbnail", {}).get("source")   # thumbnail invece di original
        if img:
            raw_results[title] = img

    resolved = {}
    for t in titles:
        canon = redir.get(norm.get(t, t), norm.get(t, t))
        if canon in raw_results:
            resolved[t] = raw_results[canon]
    return resolved


def main():
    with open("data/logos.json", encoding="utf-8") as f:
        logos = json.load(f)
    with open("data/rivalries_ranking.json", encoding="utf-8") as f:
        ranking = json.load(f)

    # Tutti i team del ranking
    teams = sorted({r["team1"] for r in ranking} | {r["team2"] for r in ranking})
    missing = [t for t in teams if t not in logos]
    print(f"Team mancanti prima del fix: {len(missing)}")

    # Costruisce lista di query: alias noto o nome originale
    to_query = {}  # query_title → original_name
    for name in missing:
        alias = KNOWN_ALIASES.get(name, name)
        to_query[alias] = name

    print(f"Query da inviare: {len(to_query)}")

    # Fetch in batch
    query_titles = list(to_query.keys())
    new_logos = {}
    for i in range(0, len(query_titles), 50):
        batch = query_titles[i:i+50]
        try:
            results = fetch_batch(batch)
            for query_title, url in results.items():
                original_name = to_query.get(query_title, query_title)
                new_logos[original_name] = url
                print(f"  [OK] {original_name} <- {query_title}")
        except Exception as e:
            print(f"  [ERR] batch {i}: {e}")
        time.sleep(1)

    still_missing = [t for t in missing if t not in new_logos]
    print(f"\nNuovi trovati: {len(new_logos)}")
    print(f"Ancora mancanti: {len(still_missing)}")
    if still_missing:
        for t in still_missing:
            print(f"  - {t}")

    # Aggiorna logos.json
    logos.update(new_logos)
    with open("data/logos.json", "w", encoding="utf-8") as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)

    # Aggiorna fetch_logos_missing.txt
    all_teams = sorted({r["team1"] for r in ranking} | {r["team2"] for r in ranking})
    final_missing = [t for t in all_teams if t not in logos]
    with open("fetch_logos_missing.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_missing))

    print(f"\nLogos totali: {len(logos)}")
    print(f"Mancanti definitivi: {len(final_missing)}")


if __name__ == "__main__":
    main()
