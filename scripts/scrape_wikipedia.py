import json
import os
import requests
import time
import re
from datetime import datetime

# Headers to be polite to Wikipedia API
HEADERS = {
    'User-Agent': 'RivalitaDataCollector/1.0 (https://github.com/marcorzzn/global-club-rivalries-ranking)'
}

def get_category_members(category_name):
    print(f"Fetching members for {category_name}...")
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category_name,
        "cmlimit": "500",
        "cmtype": "page|subcat",
        "format": "json"
    }
    
    members = []
    subcats = []
    
    while True:
        try:
            response = requests.get(url, params=params, headers=HEADERS)
            data = response.json()
            
            for item in data['query']['categorymembers']:
                if item['ns'] == 14: # Category
                    subcats.append(item['title'])
                elif item['ns'] == 0: # Page
                    members.append(item['title'])
                    
            if 'continue' in data:
                params['cmcontinue'] = data['continue']['cmcontinue']
            else:
                break
        except Exception as e:
            print(f"Error fetching category {category_name}: {e}")
            break
            
        time.sleep(0.5)
        
    return members, subcats

def get_page_summary(title, lang="en"):
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('extract', '')
    except:
        pass
    return ""

def parse_teams_from_title(title):
    # Try to extract teams from typical rivalry titles like "A.C. Milan v Juventus F.C. rivalry"
    title = title.replace(" rivalry", "").replace(" derby", "").replace(" Derby", "")
    
    # Common separators
    separators = [" v ", " vs ", "–", "-", " and "]
    for sep in separators:
        if sep in title:
            parts = title.split(sep)
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()
    return None, None

def infer_continent_country(title, subcats_path):
    # Very basic inference based on categories it belongs to
    continent = "Europe" # Default
    country = "Unknown"
    
    path_str = " ".join(subcats_path).lower()
    
    continents_map = {
        "europe": "Europe",
        "south america": "South America",
        "africa": "Africa",
        "asia": "Asia",
        "north america": "North America",
        "oceania": "Oceania"
    }
    
    for key, val in continents_map.items():
        if key in path_str:
            continent = val
            break
            
    # List of some major countries for quick matching
    countries = ["England", "Italy", "Spain", "Germany", "France", "Brazil", "Argentina", 
                 "Portugal", "Netherlands", "Turkey", "Scotland", "Mexico", "USA", "Japan"]
                 
    for c in countries:
        if c.lower() in path_str or c.lower() in title.lower():
            country = c
            break
            
    return continent, country
    
def infer_type(title, summary):
    text = (title + " " + summary).lower()
    if "city derby" in text or "local derby" in text or "cross-town" in text:
        return "city_derby"
    elif "regional" in text:
        return "regional"
    elif "international" in text:
        return "international"
    else:
        return "national"

def main():
    print("Starting Wikipedia scraper...")
    
    # Track visited categories to avoid infinite loops
    visited_cats = set()
    cats_to_visit = [("Category:Association football rivalries", [])]
    
    all_pages = set()
    page_to_path = {}
    
    # Traverse category tree (limit depth to avoid taking too long)
    max_cats = 20 # Limit for this script to finish in a reasonable time
    cats_processed = 0
    
    while cats_to_visit and cats_processed < max_cats:
        current_cat, path = cats_to_visit.pop(0)
        
        if current_cat in visited_cats:
            continue
            
        visited_cats.add(current_cat)
        cats_processed += 1
        
        members, subcats = get_category_members(current_cat)
        
        for member in members:
            all_pages.add(member)
            if member not in page_to_path:
                page_to_path[member] = path + [current_cat]
                
        for subcat in subcats:
            cats_to_visit.append((subcat, path + [current_cat]))
            
    print(f"Found {len(all_pages)} rivalry pages.")
    
    rivalries = []
    
    # Process a subset to avoid taking too long in this environment
    # In a real scenario we'd process all of them
    pages_list = list(all_pages)[:150] 
    
    for i, page_title in enumerate(pages_list):
        print(f"Processing {i+1}/{len(pages_list)}: {page_title}")
        
        summary_en = get_page_summary(page_title, "en")
        if not summary_en:
            continue
            
        summary_it = get_page_summary(page_title, "it")
        
        team1, team2 = parse_teams_from_title(page_title)
        
        if not team1 or not team2:
            # Fallback if parsing fails, just use the title and "Unknown"
            team1 = page_title.split()[0]
            team2 = "Unknown"
            
        continent, country = infer_continent_country(page_title, page_to_path.get(page_title, []))
        rtype = infer_type(page_title, summary_en)
        
        slug = page_title.replace(" ", "_").lower()
        
        rivalry = {
            "id": slug,
            "name_en": page_title.replace("_", " "),
            "name_it": page_title.replace("_", " "), # Ideally we'd translate this
            "team1": team1,
            "team2": team2,
            "continent": continent,
            "country": country,
            "league": "Unknown", # Would need more complex parsing
            "type": rtype,
            "wikipedia_url": f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
            "summary_en": summary_en,
            "summary_it": summary_it,
            "source": "Wikipedia",
            "data_retrieved": datetime.now().strftime("%Y-%m-%d")
        }
        
        rivalries.append(rivalry)
        time.sleep(0.1) # Be nice to Wikipedia
        
    os.makedirs('data', exist_ok=True)
    with open('data/rivalries_encyclopaedia.json', 'w', encoding='utf-8') as f:
        json.dump(rivalries, f, ensure_ascii=False, indent=2)
        
    print(f"Generated data/rivalries_encyclopaedia.json with {len(rivalries)} entries.")

if __name__ == "__main__":
    main()
