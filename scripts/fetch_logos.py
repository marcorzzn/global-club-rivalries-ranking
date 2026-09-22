"""
Recupera i loghi ufficiali delle squadre via Wikipedia PageImages API.
Nessuna API key richiesta. Rispetta le policy di Wikipedia (User-Agent + rate limit).

Uso:
    python3 fetch_logos.py

Legge data/rivalries_ranking.json (e opzionalmente data/rivalries_encyclopaedia.json),
estrae tutti i nomi squadra univoci, interroga Wikipedia in batch da 50,
scrive data/logos.json  { "Nome squadra": "https://url-logo.png", ... }

Le squadre per cui Wikipedia non restituisce un'immagine vengono elencate
in fetch_logos_missing.txt per controllo manuale — NON viene inventato nulla.
"""
import json
import time
import urllib.request
import urllib.parse

HEADERS = {"User-Agent": "GlobalClubRivalriesRanking/1.0 (progetto studentesco, contatto: marco)"}
API = "https://en.wikipedia.org/w/api.php"


def fetch_batch(titles):
    params = {
        "action": "query",
        "titles": "|".join(titles),
        "prop": "pageimages",
        "piprop": "thumbnail",   # thumbnail converte SVG→PNG (original non restituisce SVG)
        "pithumbsize": 300,
        "format": "json",
        "redirects": 1,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    norm = {n["from"]: n["to"] for n in data.get("query", {}).get("normalized", [])}
    redir = {r["from"]: r["to"] for r in data.get("query", {}).get("redirects", [])}
    out = {}
    for page in pages.values():
        title = page.get("title")
        img = page.get("thumbnail", {}).get("source")   # thumbnail invece di original
        if img:
            out[title] = img
    resolved = {}
    for t in titles:
        canon = redir.get(norm.get(t, t), norm.get(t, t))
        if canon in out:
            resolved[t] = out[canon]
    return resolved


def main():
    with open("data/rivalries_ranking.json", encoding="utf-8") as f:
        ranking = json.load(f)
    teams = set()
    for r in ranking:
        teams.add(r["team1"])
        teams.add(r["team2"])
    teams = sorted(teams)
    print(f"Squadre da cercare: {len(teams)}")

    logos = {}
    for i in range(0, len(teams), 50):
        batch = teams[i:i + 50]
        try:
            result = fetch_batch(batch)
            logos.update(result)
        except Exception as e:
            print(f"Errore batch {i}: {e}")
        time.sleep(1)  # rispetto rate limit Wikipedia

    missing = [t for t in teams if t not in logos]

    with open("data/logos.json", "w", encoding="utf-8") as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)
    with open("fetch_logos_missing.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(missing))

    print(f"Trovati: {len(logos)}/{len(teams)}")
    print(f"Mancanti (controllo manuale necessario): {len(missing)}")
    if missing:
        print("  ->", ", ".join(missing))


if __name__ == "__main__":
    main()
