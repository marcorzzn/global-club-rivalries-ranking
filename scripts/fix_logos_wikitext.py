"""
scripts/fix_logos_wikitext.py  — v3 (approccio corretto)

Perché pageimages ha fallito:
  - piprop=thumbnail/original: non funziona se la pagina non ha 'pageimage' impostato
    (molte pagine di club non lo hanno, inclusa Arsenal F.C.)
  - La soluzione corretta: estrai il campo 'image' dall'infobox del club nel wikitext,
    poi costruisci l'URL diretto via Special:Redirect/file

Flusso per ogni club mancante:
  1. Fetch wikitext della pagina Wikipedia del club
  2. Estrai | image = FileName.ext dall'{{Infobox football club}}
  3. URL = https://en.wikipedia.org/w/index.php?title=Special:Redirect/file/FileName.ext&width=300
     (Wikipedia lo redireziona all'URL Wikimedia Commons corretto, inclusi SVG)
  4. Salva in logos.json

NOTA: Special:Redirect/file con width= funziona per qualsiasi formato incluso SVG.
"""
import json
import re
import time
import urllib.parse
import urllib.request

HEADERS = {"User-Agent": "GlobalClubRivalriesRanking/1.0 (open source project)"}
API = "https://en.wikipedia.org/w/api.php"

# Mappa: nome team nel ranking → titolo Wikipedia esatto
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


def api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def get_club_logo_from_wikitext(wiki_title: str) -> str | None:
    """
    Estrae il filename del logo dall'infobox del club nel wikitext,
    poi restituisce l'URL Special:Redirect/file per 300px.
    Retry con backoff su 429 Too Many Requests.
    """
    for attempt in range(3):
        try:
            data = api_get({
                "action": "query",
                "titles": wiki_title,
                "prop": "revisions",
                "rvprop": "content",
                "rvslots": "main",
                "rvlimit": 1,
                "format": "json",
                "redirects": 1,
            })
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                if "missing" in page:
                    return None
                wt = (page.get("revisions") or [{}])[0] \
                         .get("slots", {}).get("main", {}).get("*", "")
                # Cerca image / logo / crest / badge nell'infobox
                patterns = [
                    r'\|\s*(?:image)\s*=\s*([^\|\n\}]+)',
                    r'\|\s*(?:logo)\s*=\s*([^\|\n\}]+)',
                    r'\|\s*(?:crest)\s*=\s*([^\|\n\}]+)',
                    r'\|\s*(?:badge)\s*=\s*([^\|\n\}]+)',
                ]
                for pat in patterns:
                    m = re.search(pat, wt[:5000], re.IGNORECASE)
                    if m:
                        raw = m.group(1).strip()
                        raw = re.sub(r'\[\[(?:File|Image):([^\|\]]+).*?\]\]', r'\1', raw, flags=re.IGNORECASE)
                        raw = re.sub(r'\{\{.*?\}\}', '', raw).strip()
                        raw = re.sub(r'^(?:File|Image):', '', raw, flags=re.IGNORECASE).strip()
                        if raw and '.' in raw and len(raw) < 200:
                            encoded = urllib.parse.quote(raw.replace(" ", "_"))
                            url = f"https://en.wikipedia.org/w/index.php?title=Special:Redirect/file/{encoded}&width=300"
                            return url
            return None  # pagina trovata ma nessun campo image
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 10 * (2 ** attempt)
                print(f"  [429] rate limit — attendo {wait}s...")
                time.sleep(wait)
            else:
                print(f"  [HTTP {e.code}] {wiki_title}")
                return None
        except Exception as e:
            print(f"  [err] {wiki_title}: {e}")
            return None
    return None


def main():
    with open("data/logos.json", encoding="utf-8") as f:
        logos = json.load(f)
    with open("data/rivalries_ranking.json", encoding="utf-8") as f:
        ranking = json.load(f)

    all_teams = sorted({r["team1"] for r in ranking} | {r["team2"] for r in ranking})
    missing = [t for t in all_teams if t not in logos]
    print(f"Team mancanti: {len(missing)}")

    found = 0
    for name in missing:
        wiki_title = KNOWN_ALIASES.get(name, name)
        print(f"  [{name}] -> Wikipedia: '{wiki_title}'")

        url = get_club_logo_from_wikitext(wiki_title)
        time.sleep(2.0)   # Wikipedia rate limit: max ~200 req/min per IP; 2s = ~30/min safe

        if url:
            logos[name] = url
            print(f"    OK: {url[:80]}...")
            found += 1
        else:
            print(f"    NESSUN LOGO TROVATO")

    print(f"\nNuovi trovati: {found}/{len(missing)}")

    with open("data/logos.json", "w", encoding="utf-8") as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)

    still_missing = [t for t in all_teams if t not in logos]
    with open("fetch_logos_missing.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(still_missing))

    print(f"Logos totali: {len(logos)}")
    print(f"Ancora mancanti: {len(still_missing)}")


if __name__ == "__main__":
    main()
