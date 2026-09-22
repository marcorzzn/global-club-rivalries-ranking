"""
scripts/fix_renamed_pages.py
Corregge le voci dell'enciclopedia che sono state aggiunte con titoli
Wikipedia non più validi (pagina inesistente o rinominata).

Problemi identificati dalla diagnosi:
  - "North West derby (association football)" → missing=True su Wikipedia EN
    La rivalità Man Utd–Liverpool è nell'enc come "Liverpool F.C.–Manchester United F.C. rivalry"
    Dobbiamo: trovare la voce corretta, aggiornare il summary del seed manuale,
    o rimuovere il seed manuale e linkarlo alla voce corretta

  - "El Gran Derbi" → missing=True su Wikipedia EN
    La rivalità Siviglia–Real Betis potrebbe essere in enc come "Seville derby"
    Stesso approccio

Soluzione: cerca nei titoli corretti, aggiorna i seed manuali.
"""
import json
import re
import urllib.parse
import urllib.request
import time

HEADERS = {"User-Agent": "GlobalClubRivalriesRanking/1.0"}
API = "https://en.wikipedia.org/w/api.php"

# Titoli Wikipedia alternativi da tentare
ALTERNATIVE_TITLES = {
    "north_west_derby": [
        "North West derby",
        "North West derby (association football)",
        "Liverpool F.C.–Manchester United F.C. rivalry",
        "Liverpool FC-Manchester United FC rivalry",
    ],
    "el_gran_derbi": [
        "Seville derby",
        "El Gran Derbi",
        "Sevilla–Real Betis rivalry",
    ],
}


def api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def find_working_title(titles: list) -> tuple[str | None, str]:
    """Trova il primo titolo Wikipedia che esiste realmente."""
    for title in titles:
        data = api_get({"action": "query", "titles": title,
                        "redirects": 1, "format": "json"})
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "missing" not in page:
                final = page.get("title", title)
                print(f"    FOUND: '{title}' -> '{final}'")
                return title, final
            else:
                print(f"    missing: '{title}'")
        time.sleep(0.3)
    return None, ""


def fetch_extract(title: str) -> str:
    data = api_get({"action": "query", "prop": "extracts",
                    "exsentences": 8, "explaintext": 1,
                    "titles": title, "format": "json", "redirects": 1})
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        return page.get("extract", "")
    return ""


def main():
    with open("data/rivalries_encyclopaedia.json", encoding="utf-8") as f:
        enc = json.load(f)

    enc_by_id = {e["id"]: i for i, e in enumerate(enc)}

    for entry_id, alt_titles in ALTERNATIVE_TITLES.items():
        print(f"\n=== {entry_id} ===")
        idx = enc_by_id.get(entry_id)
        if idx is None:
            print(f"  NON nell'enciclopedia")
            continue

        orig_title, final_title = find_working_title(alt_titles)
        if not orig_title:
            print(f"  Nessun titolo Wikipedia valido trovato — voce lasciata con summary vuoto")
            continue

        # Aggiorna wikipedia_url
        enc[idx]["wikipedia_url"] = f"https://en.wikipedia.org/wiki/{final_title.replace(' ', '_')}"

        # Fetch summary
        summary = fetch_extract(orig_title)
        time.sleep(0.4)
        enc[idx]["summary_en"] = summary
        print(f"  Summary: {len(summary)} chars")

        # IT langlinks
        data = api_get({"action": "query", "titles": orig_title,
                        "prop": "langlinks", "lllang": "it",
                        "format": "json", "redirects": 1})
        pages = data.get("query", {}).get("pages", {})
        it_title = None
        for page in pages.values():
            for ll in page.get("langlinks", []):
                if ll.get("lang") == "it":
                    it_title = ll.get("*")
        time.sleep(0.3)

        if it_title:
            it_url = f"https://it.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(it_title.replace(' ', '_'), safe='')}"
            req = urllib.request.Request(it_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as r:
                it_data = json.loads(r.read().decode("utf-8"))
            enc[idx]["summary_it"] = it_data.get("extract", "")
            enc[idx]["name_it"] = it_title
            print(f"  IT: '{it_title}' ({len(enc[idx]['summary_it'])} chars)")
        else:
            print(f"  Nessuna pagina IT ufficiale")

    with open("data/rivalries_encyclopaedia.json", "w", encoding="utf-8") as f:
        json.dump(enc, f, ensure_ascii=False, indent=2)

    print(f"\nEnciclopedia: {len(enc)} voci")


if __name__ == "__main__":
    main()
