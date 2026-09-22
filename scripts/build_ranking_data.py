"""
scripts/build_ranking_data.py  — v3
Costruisce data/rivalries_ranking.json con dati VERIFICATI da Wikipedia.

Miglioramenti v3 vs v2:
  - Fuzzy league matching (normalizzazione accenti, case-insensitive)
  - fetch_long_extract(): API extracts (20 frasi) invece del solo REST summary
    → copre i paragrafi introduttivi dove il conteggio match è quasi sempre citato
  - Aggiunte ~20 rivalità alla lista curata
  - Superclásico fix (league name con accento)
"""
import json
import re
import os
import sys
import time
import unicodedata
from datetime import datetime, timezone

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import make_id

HEADERS = {
    'User-Agent': 'RivalitaDataCollector/2.0 '
                  '(https://github.com/marcorzzn/global-club-rivalries-ranking)'
}
API_EN  = "https://en.wikipedia.org/w/api.php"
CURRENT_YEAR = 2025


# ── Leghe Opta ──────────────────────────────────────────────────────────────

def normalize_str(s: str) -> str:
    """Rimuove accenti, lowercase — per confronti fuzzy lega."""
    s = unicodedata.normalize('NFD', s)
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower().strip()


def load_leagues() -> tuple[dict, dict, int]:
    """Restituisce (raw_dict, normalized_dict, total)."""
    try:
        with open('data/leagues_opta.json', encoding='utf-8') as f:
            data = json.load(f)
        raw = {l['name']: l['rank'] for l in data['leagues']}
        norm = {normalize_str(l['name']): (l['name'], l['rank']) for l in data['leagues']}
        return raw, norm, len(data['leagues'])
    except Exception as e:
        print(f"[WARN] leagues_opta.json: {e}")
        return {}, {}, 0


def find_league(name: str, raw: dict, norm: dict) -> tuple[str | None, int | None]:
    """Cerca la lega con match esatto poi fuzzy (accenti, parziale)."""
    if name in raw:
        return name, raw[name]
    key = normalize_str(name)
    if key in norm:
        return norm[key]
    # Parziale
    for nk, (canon, rank) in norm.items():
        if key in nk or nk in key:
            return canon, rank
    return None, None


# ── Fetch Wikipedia ─────────────────────────────────────────────────────────

def fetch_wikitext(title: str) -> tuple[str, str]:
    params = {
        "action": "query", "prop": "revisions",
        "rvprop": "content", "rvslots": "main",
        "titles": title, "format": "json", "redirects": 1,
    }
    try:
        r = requests.get(API_EN, params=params, headers=HEADERS, timeout=20)
        r.raise_for_status()
        ts = datetime.now(timezone.utc).isoformat()
        pages = r.json().get('query', {}).get('pages', {})
        for page in pages.values():
            wt = (page.get('revisions') or [{}])[0] \
                     .get('slots', {}).get('main', {}).get('*', '')
            return wt, ts
    except Exception as e:
        print(f"  [wikitext err] {e}")
    return '', ''


def fetch_long_extract(title: str) -> str:
    """
    Wikipedia API extracts — prime 50 frasi (aumentato da 20).
    Cattura anche sezioni Statistics/History più lontane dall'inizio.
    """
    params = {
        "action": "query", "prop": "extracts",
        "exsentences": 50, "explaintext": 1,
        "exsectionformat": "plain",
        "titles": title, "format": "json", "redirects": 1,
    }
    try:
        r = requests.get(API_EN, params=params, headers=HEADERS, timeout=20)
        r.raise_for_status()
        pages = r.json().get('query', {}).get('pages', {})
        for page in pages.values():
            return page.get('extract', '')
    except Exception as e:
        print(f"  [extract err] {e}")
    return ''


def extract_p_raw_from_wikitext_body(wikitext: str, fields: dict) -> tuple[int | None, str]:
    """
    Ultima risorsa: cerca il conteggio nel corpo completo del wikitext.
    Strategie in ordine:
    1. W+D+L sum dai campi infobox (team1_wins + draws + team2_wins)
    2. Ricerca pattern nel testo pulito del corpo articolo
    3. W+D+L sum da tabelle wikitext (pattern || N || N || N)
    """
    # ── Strategia 1: W+D+L dall'infobox ──
    win_keys_t1 = ('team1_wins', 'wins1', 'win1', 'team_1_wins', 'p1wins')
    win_keys_t2 = ('team2_wins', 'wins2', 'win2', 'team_2_wins', 'p2wins')
    draw_keys   = ('draws', 'draw', 'ties', 'tie')
    def _num(keys):
        for k in keys:
            v = fields.get(k, '')
            if v:
                m = re.search(r'(\d+)', v)
                if m:
                    return int(m.group(1))
        return None
    w1 = _num(win_keys_t1)
    w2 = _num(win_keys_t2)
    d  = _num(draw_keys)
    if w1 is not None and w2 is not None and d is not None:
        total = w1 + w2 + d
        if 10 <= total <= 10000:
            return total, f"W+D+L sum from infobox: {w1}+{d}+{w2}={total}"

    # ── Strategia 2: corpo testo pulito ──
    # Trova la fine dell'infobox
    start = wikitext.find('{{Infobox')
    if start == -1:
        start = wikitext.find('{{infobox')
    body_start = 0
    if start != -1:
        depth = 0
        for i in range(start, len(wikitext)):
            if wikitext[i:i+2] == '{{':
                depth += 1
            elif wikitext[i:i+2] == '}}':
                depth -= 1
                if depth == 0:
                    body_start = i + 2
                    break
    body = wikitext[body_start:]
    # Pulizia markup
    text = re.sub(r'\[\[File:[^\]]+\]\]', '', body)
    text = re.sub(r'\[\[([^|\]]+\|)?([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\{\{[^{}]+\}\}', '', text)
    text = re.sub(r"'{2,3}", '', text)
    text = re.sub(r'<[^>]+>', '', text)

    for pattern in P_RAW_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            raw = m.group(1).replace(',', '')
            try:
                n = int(raw)
                if 1 <= n <= 10000:
                    snippet = text[max(0, m.start()-50):m.end()+50].strip()
                    snippet = ' '.join(snippet.split())[:100]
                    return n, f"Wikipedia article body: \"{snippet}\""
            except ValueError:
                pass

    # ── Strategia 3: W+D+L da tabelle wikitext (|| N || N || N) ──
    # Cerca righe di tabella con 3 numeri consecutivi vicino a "Total" o sezione match
    for m in re.finditer(r'(\d+)\s*\|\|\s*(\d+)\s*\|\|\s*(\d+)', body):
        nums = [int(m.group(i)) for i in (1, 2, 3)]
        total = sum(nums)
        # Sanity: tutti i valori positivi, totale in range ragionevole per rivalità
        if all(n >= 0 for n in nums) and 30 <= total <= 3000:
            context = body[max(0, m.start()-200):m.start()].lower()
            # Presenza di keyword di contesto aumenta affidabilità
            if any(kw in context for kw in ('match', 'game', 'win', 'draw', 'total', 'meeting')):
                return total, f"W+D+L sum from table: {nums[0]}+{nums[1]}+{nums[2]}={total}"

    return None, ''


# ── Parsing infobox ──────────────────────────────────────────────────────────

def parse_infobox(wikitext: str) -> dict:
    start = wikitext.find('{{Infobox')
    if start == -1:
        start = wikitext.find('{{infobox')
    if start == -1:
        return {}
    depth, end = 0, start
    for i in range(start, len(wikitext)):
        if wikitext[i:i+2] == '{{':
            depth += 1
        elif wikitext[i:i+2] == '}}':
            depth -= 1
            if depth == 0:
                end = i + 2
                break
    block = wikitext[start:end]
    fields = {}
    pat = re.compile(
        r'^\s*\|\s*([^=\n|]+?)\s*=\s*(.*?)(?=\n\s*\||\n?\}\})',
        re.MULTILINE | re.DOTALL
    )
    for m in pat.finditer(block):
        key = m.group(1).strip().lower().replace(' ', '_')
        val = m.group(2).strip()
        if val:
            fields[key] = val
    return fields


def extract_year_from_wikivalue(value: str) -> int | None:
    # Template: {{dts|YYYY|...}}, {{Date|YYYY|...}}, {{start date|YYYY|...}}
    tmpl = re.search(r'\{\{[^}|]+\|(\d{4})', value)
    if tmpl:
        yr = int(tmpl.group(1))
        if 1800 <= yr <= 2100:
            return yr
    # Anno nel testo libero
    m = re.search(r'\b(1[89]\d{2}|20[012]\d)\b', value)
    if m:
        return int(m.group())
    return None


def extract_first_year(fields: dict) -> int | None:
    for key in ('first_game', 'first_meeting', 'first_match', 'established', 'founded'):
        if key in fields:
            yr = extract_year_from_wikivalue(fields[key])
            if yr:
                return yr
    return None


def extract_last_year(fields: dict) -> tuple[int, str]:
    for key in ('latest_meeting', 'last_game', 'last_meeting', 'last_match',
                'most_recent', 'latest_game', 'next_meeting'):
        if key in fields:
            yr = extract_year_from_wikivalue(fields[key])
            if yr and yr <= CURRENT_YEAR + 1:
                return yr, 'Wikipedia infobox'
    return CURRENT_YEAR, 'assumed_ongoing_2025'


def compute_m_raw(first_year: int, last_year: int) -> int:
    return max(1, (last_year - first_year) // 10 + 1)


# ── p_raw ────────────────────────────────────────────────────────────────────

P_RAW_PATTERNS = [
    r'(\d[\d,]+)\s+(?:competitive\s+)?(?:matches|meetings|games|fixtures|encounters)',
    r'met\s+(\d[\d,]+)\s+times',
    r'played\s+(\d[\d,]+)\s+(?:times|matches|games)',
    r'faced\s+each\s+other\s+(\d[\d,]+)\s+times',
    r'(\d[\d,]+)\s+(?:official|recorded|total)\s+(?:matches|meetings|games)',
    r'(\d[\d,]+)\s+times\s+in\s+(?:all|official|competitive)',
    r'(\d[\d,]+)\s+(?:league\s+)?encounters',
    r'(\d[\d,]+)\s+head.to.head',
    r'have\s+played\s+(\d[\d,]+)',
]


def extract_p_raw_from_infobox(fields: dict) -> int | None:
    for key in ('matches', 'total_matches', 'total_games', 'total_meetings',
                'games', 'meetings', 'competitive_matches', 'encounters',
                'total', 'no_of_meetings'):
        val = fields.get(key, '')
        if val:
            digits = re.search(r'(\d[\d,]*)', val)
            if digits:
                try:
                    n = int(digits.group().replace(',', ''))
                    if 1 <= n <= 10000:
                        return n
                except ValueError:
                    pass
    return None


def extract_p_raw_from_text(text: str) -> tuple[int | None, str]:
    """Cerca il conteggio nel testo (summary o extract lungo)."""
    for pattern in P_RAW_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            raw = m.group(1).replace(',', '')
            try:
                n = int(raw)
                if 1 <= n <= 10000:
                    snippet = text[max(0, m.start()-50):m.end()+50].strip()
                    return n, snippet[:100]
            except ValueError:
                pass
    return None, ''


# ── Lista rivalità ───────────────────────────────────────────────────────────

RIVALRIES = [
    # ══ INGHILTERRA ══
    {"wt": "North London derby",
     "name_en": "North London Derby", "name_it": "Derby del Nord di Londra",
     "t1": "Arsenal FC", "t2": "Tottenham Hotspur",
     "league": "Premier League", "cont": "Europe", "country": "England", "derby": "city"},

    {"wt": "Merseyside derby",
     "name_en": "Merseyside Derby", "name_it": "Derby del Merseyside",
     "t1": "Liverpool FC", "t2": "Everton FC",
     "league": "Premier League", "cont": "Europe", "country": "England", "derby": "city"},

    {"wt": "Manchester derby",
     "name_en": "Manchester Derby", "name_it": "Derby di Manchester",
     "t1": "Manchester City", "t2": "Manchester United",
     "league": "Premier League", "cont": "Europe", "country": "England", "derby": "city"},

    {"wt": "Steel City derby",
     "name_en": "Steel City Derby", "name_it": "Derby della Citta d'Acciaio",
     "t1": "Sheffield United", "t2": "Sheffield Wednesday",
     "league": "EFL Championship", "cont": "Europe", "country": "England", "derby": "city"},

    {"wt": "South Wales derby",
     "name_en": "South Wales Derby", "name_it": "Derby del Galles del Sud",
     "t1": "Cardiff City", "t2": "Swansea City",
     "league": "EFL Championship", "cont": "Europe", "country": "Wales", "derby": "regional"},

    {"wt": "West Midlands derby",
     "name_en": "West Midlands Derby", "name_it": "Derby del West Midlands",
     "t1": "Aston Villa", "t2": "Birmingham City",
     "league": "Premier League", "cont": "Europe", "country": "England", "derby": "regional"},

    # ══ SCOZIA ══
    {"wt": "Old Firm",
     "name_en": "Old Firm", "name_it": "Old Firm",
     "t1": "Celtic FC", "t2": "Rangers FC",
     "league": "Scottish Premiership", "cont": "Europe", "country": "Scotland", "derby": "city"},

    {"wt": "Edinburgh derby",
     "name_en": "Edinburgh Derby", "name_it": "Derby di Edimburgo",
     "t1": "Heart of Midlothian FC", "t2": "Hibernian FC",
     "league": "Scottish Premiership", "cont": "Europe", "country": "Scotland", "derby": "city"},

    # ══ SPAGNA ══
    {"wt": "El Clasico",
     "name_en": "El Clasico", "name_it": "El Clasico",
     "t1": "Real Madrid", "t2": "FC Barcelona",
     "league": "La Liga", "cont": "Europe", "country": "Spain", "derby": "national"},

    {"wt": "Madrid derby",
     "name_en": "Madrid Derby", "name_it": "Derby di Madrid",
     "t1": "Real Madrid", "t2": "Atletico Madrid",
     "league": "La Liga", "cont": "Europe", "country": "Spain", "derby": "city"},

    {"wt": "El Gran Derbi",
     "name_en": "El Gran Derbi", "name_it": "Il Gran Derbi",
     "t1": "Sevilla FC", "t2": "Real Betis",
     "league": "La Liga", "cont": "Europe", "country": "Spain", "derby": "city"},

    {"wt": "Derby de Barcelona",
     "name_en": "Derby de Barcelona", "name_it": "Derby di Barcellona",
     "t1": "FC Barcelona", "t2": "RCD Espanyol",
     "league": "La Liga", "cont": "Europe", "country": "Spain", "derby": "city"},

    # ══ ITALIA ══
    {"wt": "Derby della Madonnina",
     "name_en": "Derby della Madonnina", "name_it": "Derby della Madonnina",
     "t1": "AC Milan", "t2": "FC Internazionale Milano",
     "league": "Serie A", "cont": "Europe", "country": "Italy", "derby": "city"},

    {"wt": "Derby d'Italia",
     "name_en": "Derby d'Italia", "name_it": "Derby d'Italia",
     "t1": "Juventus FC", "t2": "FC Internazionale Milano",
     "league": "Serie A", "cont": "Europe", "country": "Italy", "derby": "national"},

    {"wt": "Derby della Capitale",
     "name_en": "Derby della Capitale", "name_it": "Derby della Capitale",
     "t1": "AS Roma", "t2": "SS Lazio",
     "league": "Serie A", "cont": "Europe", "country": "Italy", "derby": "city"},

    {"wt": "Derby di Torino",
     "name_en": "Derby di Torino", "name_it": "Derby di Torino",
     "t1": "Juventus FC", "t2": "Torino FC",
     "league": "Serie A", "cont": "Europe", "country": "Italy", "derby": "city"},

    {"wt": "Derby della Lanterna",
     "name_en": "Derby della Lanterna", "name_it": "Derby della Lanterna",
     "t1": "Genoa CFC", "t2": "UC Sampdoria",
     "league": "Serie A", "cont": "Europe", "country": "Italy", "derby": "city"},

    # ══ GERMANIA ══
    {"wt": "Der Klassiker",
     "name_en": "Der Klassiker", "name_it": "Der Klassiker",
     "t1": "FC Bayern Munich", "t2": "Borussia Dortmund",
     "league": "Bundesliga", "cont": "Europe", "country": "Germany", "derby": "national"},

    {"wt": "Revierderby",
     "name_en": "Revierderby", "name_it": "Revierderby",
     "t1": "Borussia Dortmund", "t2": "FC Schalke 04",
     "league": "Bundesliga", "cont": "Europe", "country": "Germany", "derby": "regional"},

    {"wt": "Rhine derby",
     "name_en": "Rhine Derby", "name_it": "Derby del Reno",
     "t1": "1. FC Koln", "t2": "Borussia Monchengladbach",
     "league": "Bundesliga", "cont": "Europe", "country": "Germany", "derby": "regional"},

    # ══ FRANCIA ══
    {"wt": "Le Classique",
     "name_en": "Le Classique", "name_it": "Le Classique",
     "t1": "Paris Saint-Germain", "t2": "Olympique de Marseille",
     "league": "Ligue 1", "cont": "Europe", "country": "France", "derby": "national"},

    # ══ PORTOGALLO ══
    {"wt": "O Classico",
     "name_en": "O Classico", "name_it": "O Classico",
     "t1": "SL Benfica", "t2": "FC Porto",
     "league": "Primeira Liga", "cont": "Europe", "country": "Portugal", "derby": "national"},

    # ══ OLANDA ══
    {"wt": "De Klassieker",
     "name_en": "De Klassieker", "name_it": "De Klassieker",
     "t1": "AFC Ajax", "t2": "Feyenoord",
     "league": "Eredivisie", "cont": "Europe", "country": "Netherlands", "derby": "national"},

    # ══ TURCHIA ══
    {"wt": "Intercontinental derby",
     "name_en": "Intercontinental Derby", "name_it": "Derby Intercontinentale",
     "t1": "Galatasaray SK", "t2": "Fenerbahce SK",
     "league": "Super Lig", "cont": "Europe", "country": "Turkey", "derby": "city"},

    # ══ BELGIO ══
    {"wt": "RSC Anderlecht-Club Brugge KV rivalry",
     "name_en": "Belgian Classic", "name_it": "Classico Belga",
     "t1": "RSC Anderlecht", "t2": "Club Brugge KV",
     "league": "Belgian Pro League", "cont": "Europe", "country": "Belgium", "derby": "national"},

    # ══ AUSTRIA ══
    {"wt": "Vienna derby",
     "name_en": "Vienna Derby", "name_it": "Derby di Vienna",
     "t1": "SK Rapid Wien", "t2": "FK Austria Wien",
     "league": "Austrian Football Bundesliga", "cont": "Europe", "country": "Austria", "derby": "city"},

    # ══ GRECIA ══
    {"wt": "Eternal derby (Greece)",
     "name_en": "Eternal Derby (Greece)", "name_it": "Eterno Derby (Grecia)",
     "t1": "Olympiacos FC", "t2": "Panathinaikos FC",
     "league": "Super League Greece", "cont": "Europe", "country": "Greece", "derby": "city"},

    # ══ SERBIA ══
    {"wt": "Eternal derby (Serbia)",
     "name_en": "Eternal Derby (Serbia)", "name_it": "Eterno Derby (Serbia)",
     "t1": "FK Partizan", "t2": "FK Red Star Belgrade",
     "league": "Serbian SuperLiga", "cont": "Europe", "country": "Serbia", "derby": "city"},

    # ══ CROAZIA ══
    {"wt": "Eternal derby (Croatia)",
     "name_en": "Eternal Derby (Croatia)", "name_it": "Eterno Derby (Croazia)",
     "t1": "GNK Dinamo Zagreb", "t2": "HNK Hajduk Split",
     "league": "Croatian Football League", "cont": "Europe", "country": "Croatia", "derby": "national"},

    # ══ RUSSIA ══
    {"wt": "Spartak Moscow-CSKA Moscow rivalry",
     "name_en": "Moscow Derby", "name_it": "Derby di Mosca",
     "t1": "FC Spartak Moscow", "t2": "CSKA Moscow",
     "league": "Russian Premier League", "cont": "Europe", "country": "Russia", "derby": "city"},

    # ══ SUD AMERICA ══
    {"wt": "Superclasico",
     "name_en": "Superclasico", "name_it": "Superclasico",
     "t1": "Boca Juniors", "t2": "River Plate",
     "league": "Argentine Primera Division", "cont": "South America", "country": "Argentina", "derby": "city"},

    {"wt": "Fla-Flu",
     "name_en": "Fla-Flu", "name_it": "Fla-Flu",
     "t1": "Flamengo", "t2": "Fluminense",
     "league": "Brasileirao Serie A", "cont": "South America", "country": "Brazil", "derby": "city"},

    {"wt": "Paulista Derby",
     "name_en": "Paulista Derby", "name_it": "Derby Paulista",
     "t1": "Corinthians", "t2": "Palmeiras",
     "league": "Brasileirao Serie A", "cont": "South America", "country": "Brazil", "derby": "city"},

    {"wt": "Avellaneda derby",
     "name_en": "Avellaneda Derby", "name_it": "Derby di Avellaneda",
     "t1": "Racing Club de Avellaneda", "t2": "Club Atletico Independiente",
     "league": "Argentine Primera Division", "cont": "South America", "country": "Argentina", "derby": "city"},

    {"wt": "Uruguayan Clasico",
     "name_en": "Uruguayan Clasico", "name_it": "Clasico Uruguayano",
     "t1": "Club Nacional de Football", "t2": "Club Atletico Penarol",
     "league": "Uruguayan Primera Division", "cont": "South America", "country": "Uruguay", "derby": "national"},

    # ══ AFRICA ══
    {"wt": "Cairo Derby",
     "name_en": "Cairo Derby", "name_it": "Derby del Cairo",
     "t1": "Al Ahly SC", "t2": "Zamalek SC",
     "league": "Egyptian Premier League", "cont": "Africa", "country": "Egypt", "derby": "city"},

    {"wt": "Soweto derby",
     "name_en": "Soweto Derby", "name_it": "Derby di Soweto",
     "t1": "Kaizer Chiefs", "t2": "Orlando Pirates",
     "league": "South African Premier Division", "cont": "Africa", "country": "South Africa", "derby": "city"},

    {"wt": "Algiers Derby",
     "name_en": "Algiers Derby", "name_it": "Derby di Algeri",
     "t1": "CR Belouizdad", "t2": "USM Alger",
     "league": "Algerian Ligue Professionnelle 1", "cont": "Africa", "country": "Algeria", "derby": "city"},

    # ══ ASIA ══
    {"wt": "Osaka Derby",
     "name_en": "Osaka Derby", "name_it": "Derby di Osaka",
     "t1": "Gamba Osaka", "t2": "Cerezo Osaka",
     "league": "J1 League", "cont": "Asia", "country": "Japan", "derby": "city"},

    # ══ NORD AMERICA ══
    {"wt": "Hudson River Derby",
     "name_en": "Hudson River Derby", "name_it": "Derby del fiume Hudson",
     "t1": "New York City FC", "t2": "New York Red Bulls",
     "league": "Major League Soccer", "cont": "North America", "country": "USA", "derby": "city"},
]


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=== build_ranking_data.py v4 ===")
    leagues_raw, leagues_norm, total_leagues = load_leagues()
    print(f"Leghe Opta: {total_leagues}")

    ranking  = []
    excluded = []

    for i, entry in enumerate(RIVALRIES, 1):
        title = entry['wt']
        print(f"\n[{i}/{len(RIVALRIES)}] {title}")

        # Fetch wikitext (per infobox)
        wikitext, ts = fetch_wikitext(title)
        time.sleep(0.5)

        fields = parse_infobox(wikitext) if wikitext else {}

        # p_raw: infobox → extract lungo → corpo wikitext completo → escluso
        p_raw = extract_p_raw_from_infobox(fields)
        p_raw_detail = 'Wikipedia infobox field'

        if p_raw is None:
            long_text = fetch_long_extract(title)
            time.sleep(0.4)
            p_raw, snippet = extract_p_raw_from_text(long_text)
            if p_raw:
                p_raw_detail = f'Wikipedia article text: "{snippet}"'

        if p_raw is None and wikitext:
            # Ultima risorsa: W+D+L e corpo completo del wikitext
            p_raw, snippet = extract_p_raw_from_wikitext_body(wikitext, fields)
            if p_raw:
                p_raw_detail = snippet

        if p_raw is None:
            print(f"  [ESCLUSO] p_raw non trovato in nessuna fonte")
            excluded.append({"title": title, "reason": "p_raw non trovato",
                             "infobox_keys": list(fields.keys())[:12]})
            continue

        # first_year
        first_year = extract_first_year(fields)
        if first_year is None:
            # tenta nel testo
            if wikitext:
                m = re.search(r'\b(1[89]\d{2})\b', wikitext[:2000])
                if m:
                    first_year = int(m.group(1))
        if first_year is None:
            print(f"  [ESCLUSO] first_year non trovato")
            excluded.append({"title": title, "reason": "first_year non trovato", "p_raw": p_raw})
            continue

        last_year, last_year_source = extract_last_year(fields)
        m_raw = compute_m_raw(first_year, last_year)

        # League
        league_name, league_rank = find_league(entry['league'], leagues_raw, leagues_norm)
        if league_rank is None:
            print(f"  [ESCLUSO] lega '{entry['league']}' non in Opta")
            excluded.append({"title": title, "reason": f"lega non in Opta: {entry['league']}"})
            continue

        l_raw = ((total_leagues - league_rank + 1) / total_leagues) * 100

        record = {
            "id":           make_id(entry['name_en']),
            "name_en":      entry['name_en'],
            "name_it":      entry['name_it'],
            "team1":        entry['t1'],
            "team2":        entry['t2'],
            "league":       league_name,
            "league_rank":  league_rank,
            "continent":    entry['cont'],
            "country":      entry['country'],
            "derby_type":   entry['derby'],
            "p_raw":        p_raw,
            "m_raw":        m_raw,
            "first_year":   first_year,
            "last_year":    last_year,
            "l_raw":        round(l_raw, 4),
            "p_raw_source":        "Wikipedia",
            "p_raw_source_detail": p_raw_detail,
            "last_year_source":    last_year_source,
            "wikipedia_url":  f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            "data_retrieved": ts,
        }

        print(f"  [OK] p={p_raw} | {first_year}-{last_year}({last_year_source[:12]}) | m={m_raw} | l={l_raw:.1f} | lega:{league_name}")
        ranking.append(record)

    # Deduplicazione per id (nel caso ci siano titoli alternativi che puntano alla stessa rivalità)
    seen = {}
    unique = []
    for r in ranking:
        if r['id'] not in seen:
            seen[r['id']] = True
            unique.append(r)
        else:
            print(f"  [DUP] {r['id']} — rimosso duplicato")

    os.makedirs('data', exist_ok=True)
    with open('data/rivalries_ranking.json', 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    with open('data/ranking_excluded.json', 'w', encoding='utf-8') as f:
        json.dump(excluded, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Incluse: {len(unique)}")
    print(f"Escluse: {len(excluded)}")

    from collections import Counter
    c = Counter(e['reason'].split(' non')[0] for e in excluded)
    for reason, count in c.most_common():
        print(f"  {count}x {reason}")


if __name__ == "__main__":
    main()
