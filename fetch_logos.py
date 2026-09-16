import os
import re
import requests
import time

def run():
    html_path = 'index.html'
    logos_dir = 'logos'
    
    if not os.path.exists(logos_dir):
        os.makedirs(logos_dir)
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    pattern = r'"name":\s*"([^"]+)",\s*"short":\s*"([^"]+)"'
    matches = re.findall(pattern, html)
    
    clubs = {}
    for name, short in matches:
        clubs[short] = name
        
    print(f"Found {len(clubs)} unique clubs.")
    
    for short_name, club_name in clubs.items():
        logo_path = os.path.join(logos_dir, f"{short_name}.png")
        if os.path.exists(logo_path):
            continue
            
        print(f"Fetching logo for {club_name} ({short_name})...")
        try:
            search_name = club_name.replace('FC ', '').replace(' FC', '').replace('CF', '').strip()
            url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={search_name}"
            r = requests.get(url, timeout=10)
            data = r.json()
            
            if data and data.get('teams'):
                badge_url = data['teams'][0].get('strBadge')
                if badge_url:
                    img_data = requests.get(badge_url, timeout=10).content
                    with open(logo_path, 'wb') as img_file:
                        img_file.write(img_data)
                    print(f"  -> Saved {short_name}.png")
                else:
                    print("  -> No badge found.")
            else:
                print("  -> Team not found.")
        except Exception as e:
            print(f"  -> Error: {e}")
            
        time.sleep(0.5)
        
if __name__ == '__main__':
    run()
