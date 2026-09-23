"""
scripts/refresh_logos.py
Ri-fetcha i loghi di TUTTI i team del ranking usando esclusivamente
il metodo wikitext (| image = dall'infobox del club).

Perché ri-fare tutti e non solo i 3 errati:
  - Non abbiamo metadati su quale logo è stato ottenuto con quale metodo.
  - Il metodo wikitext è il più accurato: legge il campo specifico dell'infobox.
  - Meglio sovrascrivere tutti con la fonte corretta piuttosto che tenere
    22 loghi di qualità incerta.

Filtro anti-falsi-positivi (LOGO_BAD_PATTERNS):
  Scarta qualunque filename che contiene pattern noti di non-loghi:
  - foto di stadi, partite, collage storici, foto di squadre.
  Se il filename non supera il filtro → logo impostato a None (null esplicito).

Rate limit: 2s tra le richieste + backoff esponenziale su 429.
"""
import json
import re
import time
import urllib.parse
import urllib.error
import urllib.request

HEADERS = {"User-Agent": "GlobalClubRivalriesRanking/1.0 (open source)"}
API = "https://en.wikipedia.org/w/api.php"

# Pattern nei filename che indicano NON-loghi
LOGO_BAD_PATTERNS = [
    'stadio', 'stadium', 'stade', 'stadion',
    '_v_', ' v ', '-vs-', '_vs_',
    'through_the_ages', 'through the ages',
    'match', 'squad', 'team_photo', 'team photo',
    'ground', 'pitch', 'training',
    'panorama', 'panoramic',
    'aerial', 'aeria',
    'fan', 'crowd', 'supporter',
    '.jpg',  # i badge veri sono quasi sempre SVG o PNG piccoli; JPG foto è sospetto
    # eccezione: alcuni badge legittimi sono JPG → gestita sotto (solo se piccolo)
]

# Pattern che fanno ECCEZIONE alla regola .jpg (badge legittimi in JPG)
LOGO_JPG_EXCEPTIONS = [
    'crest', 'badge', 'logo', 'emblem', 'shield', 'arms', 'escudo',
]

KNOWN_ALIASES = {
    "Arsenal FC":             "Arsenal F.C.",
    "AS Roma":                "A.S. Roma",
    "Celtic FC":              "Celtic F.C.",
    "Rangers FC":             "Rangers F.C.",
    "Atletico Madrid":        "Atlético de Madrid",
    "Everton FC":             "Everton F.C.",
    "Liverpool FC":           "Liverpool F.C.",
    "Manchester City":        "Manchester City F.C.",
    "Manchester United":      "Manchester United F.C.",
    "Tottenham Hotspur":      "Tottenham Hotspur F.C.",
    "Cardiff City":           "Cardiff City F.C.",
    "Swansea City":           "Swansea City A.F.C.",
    "Sheffield United":       "Sheffield United F.C.",
    "Sheffield Wednesday":    "Sheffield Wednesday F.C.",
    "Heart of Midlothian FC": "Heart of Midlothian F.C.",
    "Hibernian FC":           "Hibernian F.C.",
    "FC Porto":               "FC Porto",
    "SL Benfica":             "S.L. Benfica",
    "RSC Anderlecht":         "R.S.C. Anderlecht",
    "Real Madrid":            "Real Madrid CF",
    "River Plate":            "Club Atlético River Plate",
    "Al Ahly SC":             "Al Ahly SC",
    "Zamalek SC":             "Zamalek SC",
    "Kaizer Chiefs":          "Kaizer Chiefs F.C.",
    "Orlando Pirates":        "Orlando Pirates F.C.",
    "New York Red Bulls":     "New York Red Bulls",
    "UC Sampdoria":           "U.C. Sampdoria",
    "Cerezo Osaka":           "Cerezo Osaka",
    # Questi non erano negli alias precedenti ma sono nel ranking
    "AC Milan":               "A.C. Milan",
    "FC Internazionale Milano": "Inter Milan",
    "Juventus FC":            "Juventus F.C.",
    "Torino FC":              "Torino F.C.",
    "Genoa CFC":              "Genoa C.F.C.",
    "SS Lazio":               "S.S. Lazio",
    "UC Sampdoria":           "U.C. Sampdoria",
    "AFC Ajax":               "AFC Ajax",
    "Feyenoord":              "Feyenoord",
    "Club Brugge KV":         "Club Brugge KV",
    "Borussia Dortmund":      "Borussia Dortmund",
    "FC Schalke 04":          "FC Schalke 04",
    "FC Bayern Munich":       "FC Bayern Munich",
    "Boca Juniors":           "Boca Juniors",
    "Flamengo":               "Clube de Regatas do Flamengo",
    "Fluminense":             "Fluminense FC",
    "SK Rapid Wien":          "SK Rapid Wien",
    "FK Austria Wien":        "FK Austria Wien",
    "Olympique de Marseille": "Olympique de Marseille",
    "Paris Saint-Germain":    "Paris Saint-Germain F.C.",
    "Heart of Midlothian FC": "Heart of Midlothian F.C.",
    "Hibernian FC":           "Hibernian F.C.",
    "Al Ahly SC":             "Al Ahly SC",
    "Zamalek SC":             "Zamalek SC",
    "Kaizer Chiefs":          "Kaizer Chiefs F.C.",
    "Orlando Pirates":        "Orlando Pirates F.C.",
    "Gamba Osaka":            "Gamba Osaka",
    "New York City FC":       "New York City FC",
}


def is_logo_filename(filename: str) -> bool:
    """
    Restituisce True se il filename sembra un logo legittimo.
    Restituisce False se contiene pattern di foto/collage.
    """
    fl = filename.lower()

    # JPG accettato solo se ha keyword di badge nel nome
    if fl.endswith('.jpg') or fl.endswith('.jpeg'):
        if not any(exc in fl for exc in LOGO_JPG_EXCEPTIONS):
            return False  # JPG senza keyword → probabilmente foto

    # Controlla pattern non-logo (SVG/PNG)
    for pat in LOGO_BAD_PATTERNS:
        if pat.lower() in fl:
            # Eccezione: se il pattern è '.jpg' è già gestito sopra
            if pat == '.jpg':
                continue
            return False

    return True


def api_get(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def get_logo_from_wikitext(wiki_title: str) -> tuple[str | None, str]:
    """
    Restituisce (url, filename) oppure (None, motivo).
    """
    for attempt in range(4):
        try:
            data = api_get({
                "action": "query", "titles": wiki_title,
                "prop": "revisions", "rvprop": "content",
                "rvslots": "main", "rvlimit": 1,
                "format": "json", "redirects": 1,
            })
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                if "missing" in page:
                    return None, "pagina mancante"
                wt = (page.get("revisions") or [{}])[0] \
                         .get("slots", {}).get("main", {}).get("*", "")
                patterns = [
                    r'\|\s*image\s*=\s*([^\|\n\}]+)',
                    r'\|\s*logo\s*=\s*([^\|\n\}]+)',
                    r'\|\s*crest\s*=\s*([^\|\n\}]+)',
                    r'\|\s*badge\s*=\s*([^\|\n\}]+)',
                ]
                for pat in patterns:
                    m = re.search(pat, wt[:6000], re.IGNORECASE)
                    if m:
                        raw = m.group(1).strip()
                        # Strip [[File:...]] wrapper
                        raw = re.sub(r'\[\[(?:File|Image):([^\|\]]+).*?\]\]',
                                     r'\1', raw, flags=re.IGNORECASE)
                        # Strip template wrappers
                        raw = re.sub(r'\{\{.*?\}\}', '', raw).strip()
                        # Strip File: / Image: prefix
                        raw = re.sub(r'^(?:File|Image):', '', raw,
                                     flags=re.IGNORECASE).strip()
                        if not raw or '.' not in raw or len(raw) > 200:
                            continue
                        # Controlla filtro anti-falsi-positivi
                        if not is_logo_filename(raw):
                            return None, f"SCARTATO (non-logo): {raw}"
                        encoded = urllib.parse.quote(raw.replace(" ", "_"))
                        url = (f"https://en.wikipedia.org/w/index.php"
                               f"?title=Special:Redirect/file/{encoded}&width=300")
                        return url, raw
                return None, "nessun campo image nell'infobox"

        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 10 * (2 ** attempt)
                print(f"    [429] attendo {wait}s...")
                time.sleep(wait)
            else:
                return None, f"HTTP {e.code}"
        except Exception as e:
            return None, str(e)
    return None, "max retry raggiunto"


def main():
    with open("data/rivalries_ranking.json", encoding="utf-8") as f:
        ranking = json.load(f)
    with open("data/logos.json", encoding="utf-8") as f:
        logos = json.load(f)

    all_teams = ["Genoa CFC", "SS Lazio", "Torino FC"]
    print(f"Team nel ranking (limitato): {len(all_teams)}")
    print(f"Logo attuali in logos.json: {len(logos)}\n")

    ok = 0
    rejected = 0
    missing = 0

    for name in all_teams:
        wiki_title = KNOWN_ALIASES.get(name, name)
        url, detail = get_logo_from_wikitext(wiki_title)
        time.sleep(2.0)

        if url:
            logos[name] = url
            print(f"  [OK] {name:35} | {detail}")
            ok += 1
        else:
            if "SCARTATO" in detail:
                logos[name] = None  # null esplicito
                print(f"  [NO] {name:35} | {detail}")
                rejected += 1
            else:
                logos[name] = None
                print(f"  [--] {name:35} | {detail}")
                missing += 1

    print(f"\n{'='*50}")
    print(f"OK (logo wikitext):         {ok}")
    print(f"Scartati (non-logo):        {rejected}")
    print(f"Mancanti (pagina assente):  {missing}")
    print(f"Totale:                     {len(all_teams)}")

    with open("data/logos.json", "w", encoding="utf-8") as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)

    # Aggiorna missing list
    still_missing = [t for t in all_teams if not logos.get(t)]
    with open("fetch_logos_missing.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(still_missing))
    print(f"Mancanti/null: {len(still_missing)}")


if __name__ == "__main__":
    main()
