"""
scripts/scrape_wikipedia.py
Raccolta completa delle rivalità calcistiche da Wikipedia.

Produce: data/rivalries_encyclopaedia.json

Caratteristiche:
- Traversata COMPLETA dell'albero delle sottocategorie (nessun limite artificiale)
- Filtro noise via utils.is_noise_page()
- Id canonici via utils.make_id()
- Per ogni voce: data_retrieved = timestamp ISO esatto della consultazione di QUELLA pagina
- summary_it lasciato "" se non esiste pagina italiana (non viene inventato nulla)
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests

# Aggiungi la directory scripts al path per importare utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import make_id, is_noise_page

HEADERS = {
    'User-Agent': 'RivalitaDataCollector/2.0 '
                  '(https://github.com/marcorzzn/global-club-rivalries-ranking; '
                  'progetto open source non commerciale)'
}
API_EN = "https://en.wikipedia.org/w/api.php"
API_IT = "https://it.wikipedia.org/w/api.php"
REST_EN = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
REST_IT = "https://it.wikipedia.org/api/rest_v1/page/summary/{}"


# ── Traversata categorie ────────────────────────────────────────────────────

def get_category_members(category_name: str):
    """Restituisce (members, subcats) per una categoria Wikipedia."""
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category_name,
        "cmlimit": "500",
        "cmtype": "page|subcat",
        "format": "json"
    }
    members, subcats = [], []
    while True:
        try:
            r = requests.get(API_EN, params=params, headers=HEADERS, timeout=20)
            r.raise_for_status()
            data = r.json()
            for item in data['query']['categorymembers']:
                if item['ns'] == 14:
                    subcats.append(item['title'])
                elif item['ns'] == 0:
                    members.append(item['title'])
            if 'continue' in data:
                params['cmcontinue'] = data['continue']['cmcontinue']
            else:
                break
        except Exception as e:
            print(f"  [WARN] Categoria {category_name}: {e}")
            break
        time.sleep(0.4)
    return members, subcats


def collect_all_pages(root_category: str):
    """
    BFS completo sull'albero delle sottocategorie.
    Nessun limite di profondità o numero di categorie.
    Restituisce: { page_title: [path di categorie] }
    """
    visited = set()
    queue = [(root_category, [])]
    page_to_path = {}
    cats_done = 0

    while queue:
        cat, path = queue.pop(0)
        if cat in visited:
            continue
        visited.add(cat)
        cats_done += 1
        print(f"  [{cats_done}] {cat}")

        members, subcats = get_category_members(cat)
        for m in members:
            if m not in page_to_path:
                page_to_path[m] = path + [cat]
        for sub in subcats:
            queue.append((sub, path + [cat]))

    print(f"Totale categorie visitate: {cats_done}")
    print(f"Totale pagine trovate (prima del filtro): {len(page_to_path)}")
    return page_to_path


# ── Fetch riassunto ─────────────────────────────────────────────────────────

def get_summary(title: str, lang: str = "en") -> tuple[str, str]:
    """
    Restituisce (extract, data_retrieved_iso).
    data_retrieved è il timestamp ESATTO della chiamata API per questa pagina.
    Restituisce ("", "") se la pagina non esiste nella lingua richiesta.
    """
    url = (REST_EN if lang == "en" else REST_IT).format(
        requests.utils.quote(title, safe='')
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            retrieved_at = datetime.now(timezone.utc).isoformat()
            return r.json().get('extract', ''), retrieved_at
        return '', ''
    except Exception:
        return '', ''


# ── Inferenza metadati ──────────────────────────────────────────────────────

def infer_continent(subcats_path: list[str]) -> str:
    path = ' '.join(subcats_path).lower()
    if 'europe' in path:                           return 'Europe'
    if 'south america' in path:                    return 'South America'
    if 'africa' in path:                           return 'Africa'
    if 'asia' in path:                             return 'Asia'
    if 'north america' in path or 'concacaf' in path: return 'North America'
    if 'oceania' in path or 'australia' in path:   return 'Oceania'
    return 'Europe'  # default conservativo


COUNTRY_PATTERNS = [
    # Ordine importante: più specifici prima
    ("England",          ["england", "english"]),
    ("Scotland",         ["scotland", "scottish"]),
    ("Italy",            ["italy", "italian", "serie a"]),
    ("Spain",            ["spain", "spanish", "la liga"]),
    ("Germany",          ["germany", "german", "bundesliga"]),
    ("France",           ["france", "french", "ligue"]),
    ("Brazil",           ["brazil", "brazilian", "brasileir"]),
    ("Argentina",        ["argentina", "argentine"]),
    ("Portugal",         ["portugal", "portuguese"]),
    ("Netherlands",      ["netherlands", "dutch", "eredivisie"]),
    ("Turkey",           ["turkey", "turkish"]),
    ("Mexico",           ["mexico", "mexican", "liga mx"]),
    ("USA",              ["united states", "usa", "mls", "american soccer"]),
    ("Japan",            ["japan", "japanese", "j1 league"]),
    ("South Korea",      ["south korea", "korean", "k league"]),
    ("Australia",        ["australia", "a-league"]),
    ("Egypt",            ["egypt", "egyptian"]),
    ("South Africa",     ["south africa", "psl"]),
    ("Algeria",          ["algeria", "algerian"]),
    ("Morocco",          ["morocco", "moroccan"]),
    ("Greece",           ["greece", "greek"]),
    ("Belgium",          ["belgium", "belgian"]),
    ("Sweden",           ["sweden", "swedish"]),
    ("Norway",           ["norway", "norwegian"]),
    ("Denmark",          ["denmark", "danish"]),
    ("Poland",           ["poland", "polish"]),
    ("Russia",           ["russia", "russian"]),
    ("Ukraine",          ["ukraine", "ukrainian"]),
    ("Austria",          ["austria", "austrian"]),
    ("Switzerland",      ["switzerland", "swiss"]),
    ("Czech Republic",   ["czech"]),
    ("Serbia",           ["serbia", "serbian"]),
    ("Croatia",          ["croatia", "croatian"]),
    ("Albania",          ["albania", "albanian"]),
    ("Israel",           ["israel", "israeli"]),
    ("Iran",             ["iran", "iranian"]),
    ("Saudi Arabia",     ["saudi"]),
    ("Colombia",         ["colombia", "colombian"]),
    ("Chile",            ["chile", "chilean"]),
    ("Uruguay",          ["uruguay", "uruguayan"]),
    ("Ecuador",          ["ecuador"]),
    ("Peru",             ["peru", "peruvian"]),
    ("Bolivia",          ["bolivia"]),
    ("Costa Rica",       ["costa rica"]),
    ("Indonesia",        ["indonesia"]),
    ("Vietnam",          ["vietnam"]),
    ("Thailand",         ["thailand", "thai"]),
]


def infer_country(title: str, subcats_path: list[str]) -> str:
    text = (title + ' ' + ' '.join(subcats_path)).lower()
    for country, keywords in COUNTRY_PATTERNS:
        if any(kw in text for kw in keywords):
            return country
    return 'Unknown'


def infer_type(title: str, summary: str) -> str:
    text = (title + ' ' + summary).lower()
    if any(w in text for w in ('city derby', 'local derby', 'cross-town', 'intracity', 'stesso comune')):
        return 'city_derby'
    if 'regional' in text:
        return 'regional'
    if 'international' in text:
        return 'international'
    return 'national'


def parse_teams_from_title(title: str) -> tuple[str | None, str | None]:
    """Estrae team1 e team2 da titoli del tipo 'A v B rivalry'."""
    cleaned = re.sub(
        r'\b(rivalry|derby|clásico|clasico|classico|klassiker|classieker|classique)\b',
        '', title, flags=re.IGNORECASE
    ).strip()
    for sep in (' v ', ' vs ', ' – ', ' - ', '–', ' and ', ' \u2013 '):
        if sep in cleaned:
            parts = [p.strip() for p in cleaned.split(sep, 1)]
            if len(parts) == 2 and parts[0] and parts[1]:
                return parts[0], parts[1]
    return None, None


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=== scrape_wikipedia.py — avvio ===")
    print("Raccolta categorie (nessun limite)...")

    page_to_path = collect_all_pages("Category:Association football rivalries")

    # Filtra noise
    before = len(page_to_path)
    page_to_path = {t: p for t, p in page_to_path.items() if not is_noise_page(t)}
    print(f"Pagine dopo filtro noise: {len(page_to_path)} (rimosse: {before - len(page_to_path)})")

    rivalries = []
    titles = sorted(page_to_path.keys())

    for i, title in enumerate(titles, 1):
        print(f"[{i}/{len(titles)}] {title}")

        summary_en, retrieved_en = get_summary(title, 'en')
        if not summary_en:
            print(f"  → skip (nessun riassunto EN)")
            continue

        summary_it, _ = get_summary(title, 'it')

        team1, team2 = parse_teams_from_title(title)

        path = page_to_path[title]
        continent = infer_continent(path)
        country   = infer_country(title, path)
        rtype     = infer_type(title, summary_en)

        rivalry = {
            "id":           make_id(title),
            "name_en":      title,
            "name_it":      title,        # rimane uguale; batch traduzioni in Fix 5
            "team1":        team1,
            "team2":        team2,
            "continent":    continent,
            "country":      country,
            "league":       None,         # non inferibile affidabilmente dal titolo
            "type":         rtype,
            "wikipedia_url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            "summary_en":   summary_en,
            "summary_it":   summary_it,   # "" se non trovato (non inventato)
            "source":       "Wikipedia",
            "data_retrieved": retrieved_en   # timestamp ESATTO della consultazione
        }
        rivalries.append(rivalry)
        time.sleep(0.15)

    os.makedirs('data', exist_ok=True)
    out = 'data/rivalries_encyclopaedia.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(rivalries, f, ensure_ascii=False, indent=2)

    print(f"\n✓ {out}: {len(rivalries)} voci")


if __name__ == "__main__":
    main()
