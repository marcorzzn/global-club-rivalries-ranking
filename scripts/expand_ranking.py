import json
import os
import re
import time
import urllib.parse
from datetime import datetime, timezone

# We will import the parsing logic from build_ranking_data
import build_ranking_data as brm
from utils import make_id

def clean_wikilinks(text):
    text = re.sub(r'\[\[[^\]|]+\|([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    return text

import requests

def safe_fetch_wikitext(title):
    params = {
        "action": "query", "prop": "revisions",
        "rvprop": "content", "rvslots": "main",
        "titles": title, "format": "json", "redirects": 1,
    }
    r = requests.get(brm.API_EN, params=params, headers=brm.HEADERS, timeout=20)
    if r.status_code == 429:
        print("\n[RATE LIMIT 429] STOPPING SCRIPT.")
        raise Exception("429 Too Many Requests")
    r.raise_for_status()
    ts = datetime.now(timezone.utc).isoformat()
    pages = r.json().get('query', {}).get('pages', {})
    for page in pages.values():
        wt = (page.get('revisions') or [{}])[0].get('slots', {}).get('main', {}).get('*', '')
        return wt, ts
    return '', ''

def safe_fetch_long_extract(title):
    params = {
        "action": "query", "prop": "extracts",
        "exsentences": 50, "explaintext": 1,
        "exsectionformat": "plain",
        "titles": title, "format": "json", "redirects": 1,
    }
    r = requests.get(brm.API_EN, params=params, headers=brm.HEADERS, timeout=20)
    if r.status_code == 429:
        print("\n[RATE LIMIT 429] STOPPING SCRIPT.")
        raise Exception("429 Too Many Requests")
    r.raise_for_status()
    pages = r.json().get('query', {}).get('pages', {})
    for page in pages.values():
        return page.get('extract', '')
    return ''

def main():
    print("=== expand_ranking.py ===")

    
    with open('data/rivalries_ranking.json', encoding='utf-8') as f:
        existing_ranking = json.load(f)
    existing_ids = {r['id'] for r in existing_ranking}
    
    with open('data/ranking_excluded.json', encoding='utf-8') as f:
        try:
            excluded = json.load(f)
        except Exception:
            excluded = []
            
    excluded_titles = {e['title'].lower() for e in excluded if 'title' in e}
    
    with open('data/rivalries_encyclopaedia.json', encoding='utf-8') as f:
        encyclopaedia = json.load(f)
        
    leagues_raw, leagues_norm, total_leagues = brm.load_leagues()
    
    # Sort leagues by length descending to match longest names first in text search
    sorted_league_names = sorted(leagues_raw.keys(), key=len, reverse=True)
    sorted_norm_leagues = sorted(leagues_norm.keys(), key=len, reverse=True)
    
    new_ranking = []
    new_excluded = []
    
    # Limit number of API calls to avoid 429 if there are too many. 
    # But user said "do it with same rigor". We will use time.sleep(1) between requests.
    count = 0
    for entry in encyclopaedia:
        if entry['id'] in existing_ids:
            continue
            
        count += 1
        title = urllib.parse.unquote(entry['wikipedia_url'].split('/')[-1]).replace('_', ' ')
        print(f"\n[{count}] {title}")
        
        if title.lower() in excluded_titles:
            print("  [SKIPPED] Already in excluded list")
            continue
        
        # 1. Skip non club-vs-club heuristically
        lower_title = title.lower()
        if "messi" in lower_title or "ronaldo" in lower_title or "pelé" in lower_title or "maradona" in lower_title:
            new_excluded.append({"title": title, "reason": "Non-club rivalry (player)"})
            print("  [ESCLUSO] Player rivalry")
            continue
            
        if "national" in lower_title and "derby" not in lower_title:
            # might be national team. But we'll rely on infobox team1/team2 too.
            pass
            
        # Fetch wikitext
        try:
            wikitext, ts = safe_fetch_wikitext(title)
        except Exception as e:
            print(f"  [ERR] wikitext exception: {e}")
            if "429" in str(e):
                break
            continue
        time.sleep(1.2) # Conservative sleep to avoid 429
        
        if not wikitext:
            new_excluded.append({"title": title, "reason": "No wikitext found"})
            print("  [ESCLUSO] No wikitext")
            continue
            
        fields = brm.parse_infobox(wikitext)
        
        # Check team1 / team2
        team1 = entry.get('team1')
        team2 = entry.get('team2')
        if not team1:
            team1 = clean_wikilinks(fields.get('team1', fields.get('club1', ''))).strip()
        if not team2:
            team2 = clean_wikilinks(fields.get('team2', fields.get('club2', ''))).strip()
            
        if not team1 or not team2:
            new_excluded.append({"title": title, "reason": "team1 or team2 missing or national team"})
            print("  [ESCLUSO] team1 or team2 missing")
            continue
            
        # P_RAW
        p_raw = brm.extract_p_raw_from_infobox(fields)
        p_raw_detail = 'Wikipedia infobox field'
        
        if p_raw is None:
            try:
                long_text = safe_fetch_long_extract(title)
            except Exception as e:
                print(f"  [ERR] long_text exception: {e}")
                if "429" in str(e):
                    break
                continue
            time.sleep(0.8)
            p_raw, snippet = brm.extract_p_raw_from_text(long_text)
            if p_raw:
                p_raw_detail = f'Wikipedia article text: "{snippet}"'
                
        if p_raw is None and wikitext:
            p_raw, snippet = brm.extract_p_raw_from_wikitext_body(wikitext, fields)
            if p_raw:
                p_raw_detail = snippet
                
        if p_raw is None:
            new_excluded.append({"title": title, "reason": "p_raw non trovato", "p_raw": None})
            print("  [ESCLUSO] p_raw non trovato")
            continue
            
        # first_year
        first_year = brm.extract_first_year(fields)
        if first_year is None:
            m = re.search(r'\b(1[89]\d{2})\b', wikitext[:2000])
            if m:
                first_year = int(m.group(1))
        if first_year is None:
            new_excluded.append({"title": title, "reason": "first_year non trovato", "p_raw": p_raw})
            print("  [ESCLUSO] first_year non trovato")
            continue
            
        last_year, last_year_source = brm.extract_last_year(fields)
        m_raw = brm.compute_m_raw(first_year, last_year)
        
        # LEAGUE extraction
        league_name = entry.get('league')
        league_rank = None
        
        if not league_name or league_name == "Unknown":
            comp = fields.get('competition', fields.get('competitions', fields.get('league', '')))
            comp = clean_wikilinks(comp)
            # Find matching league in infobox
            if comp:
                for l_name in sorted_league_names:
                    if l_name.lower() in comp.lower():
                        league_name, league_rank = brm.find_league(l_name, leagues_raw, leagues_norm)
                        break
            
            # Stricter fallback: only search summary_en, not whole article
            if league_rank is None:
                summary = entry.get('summary_en', '')
                for l_name in sorted_league_names:
                    # skip generic names like "Liga I", "Serie B" in free text unless very confident
                    if len(l_name) > 8 and l_name.lower() in summary.lower():
                        league_name, league_rank = brm.find_league(l_name, leagues_raw, leagues_norm)
                        break
        else:
            league_name, league_rank = brm.find_league(league_name, leagues_raw, leagues_norm)
            
        if league_rank is None:
            new_excluded.append({"title": title, "reason": "lega non in Opta o sconosciuta", "p_raw": p_raw})
            print(f"  [ESCLUSO] lega sconosciuta/non in Opta")
            continue
            
        # compute l_raw
        l_raw = ((total_leagues - league_rank + 1) / total_leagues) * 100
        
        derby_type = entry.get('type', 'city_derby').replace('_derby', '')
        if derby_type not in ['city', 'regional', 'national']:
            derby_type = 'city'
            
        record = {
            "id":           entry['id'],
            "name_en":      entry['name_en'],
            "name_it":      entry['name_it'],
            "team1":        team1,
            "team2":        team2,
            "league":       league_name,
            "league_rank":  league_rank,
            "continent":    entry.get('continent', 'Unknown'),
            "country":      entry.get('country', 'Unknown'),
            "derby_type":   derby_type,
            "p_raw":        p_raw,
            "m_raw":        m_raw,
            "first_year":   first_year,
            "last_year":    last_year,
            "l_raw":        round(l_raw, 4),
            "p_raw_source":        "Wikipedia",
            "p_raw_source_detail": p_raw_detail,
            "last_year_source":    last_year_source,
            "wikipedia_url":  entry['wikipedia_url'],
            "data_retrieved": ts,
        }
        
        print(f"  [INCLUSO] {team1} vs {team2} | p={p_raw} | lega: {league_name}")
        new_ranking.append(record)

    # Save
    combined_ranking = existing_ranking + new_ranking
    combined_excluded = excluded + new_excluded
    
    with open('data/rivalries_ranking.json', 'w', encoding='utf-8') as f:
        json.dump(combined_ranking, f, ensure_ascii=False, indent=2)
        
    with open('data/ranking_excluded.json', 'w', encoding='utf-8') as f:
        json.dump(combined_excluded, f, ensure_ascii=False, indent=2)
        
    print(f"\nAdded {len(new_ranking)} to ranking.")
    print(f"Added {len(new_excluded)} to excluded.")

if __name__ == "__main__":
    main()
