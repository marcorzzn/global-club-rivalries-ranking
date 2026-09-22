"""
Diagnosi rapida:
1. Verifica titoli Wikipedia per North West Derby e El Gran Derbi
2. Test singolo club (Arsenal F.C.) con pageimages per capire il problema SVG
"""
import json
import urllib.request
import urllib.parse

HEADERS = {"User-Agent": "GlobalClubRivalriesRanking/1.0"}
API = "https://en.wikipedia.org/w/api.php"

def api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))

# Test 1: exists check for North West Derby
print("=== North West Derby redirect check ===")
r = api_get({"action":"query","titles":"North West derby (association football)","redirects":1,"format":"json"})
pages = r.get("query",{}).get("pages",{})
for page in pages.values():
    print(f"  pageid={page.get('pageid')} title={page.get('title')} missing={'missing' in page}")
print("  redirects:", r.get("query",{}).get("redirects",[]))

# Test 2: exists check for El Gran Derbi
print("\n=== El Gran Derbi redirect check ===")
r = api_get({"action":"query","titles":"El Gran Derbi","redirects":1,"format":"json"})
pages = r.get("query",{}).get("pages",{})
for page in pages.values():
    print(f"  pageid={page.get('pageid')} title={page.get('title')} missing={'missing' in page}")
print("  redirects:", r.get("query",{}).get("redirects",[]))

# Test 3: pageimages (thumbnail) for Arsenal F.C.
print("\n=== Arsenal F.C. pageimages thumbnail ===")
r = api_get({"action":"query","titles":"Arsenal F.C.","prop":"pageimages",
             "piprop":"thumbnail","pithumbsize":300,"format":"json","redirects":1})
pages = r.get("query",{}).get("pages",{})
for page in pages.values():
    print(f"  title={page.get('title')}")
    print(f"  thumbnail={page.get('thumbnail')}")
    print(f"  pageimage={page.get('pageimage')}")

# Test 4: wikitext image field for Arsenal F.C.
print("\n=== Arsenal F.C. wikitext image field ===")
import re
r = api_get({"action":"query","titles":"Arsenal F.C.","prop":"revisions",
             "rvprop":"content","rvslots":"main","rvlimit":1,"rvsection":0,"format":"json","redirects":1})
pages = r.get("query",{}).get("pages",{})
for page in pages.values():
    wt = (page.get("revisions") or [{}])[0].get("slots",{}).get("main",{}).get("*","")
    # Trova image = nel wikitext
    m = re.search(r'\|\s*(?:image|logo)\s*=\s*([^\|\n\}]+)', wt, re.IGNORECASE)
    if m:
        filename = m.group(1).strip()
        print(f"  image field: '{filename}'")
        # Costruisci URL thumbnail
        encoded = urllib.parse.quote(filename.replace(" ","_"))
        url = f"https://en.wikipedia.org/w/index.php?title=Special:Redirect/file/{encoded}&width=300"
        print(f"  redirect URL: {url}")
    else:
        print(f"  no image field found in first section (wikitext len={len(wt)})")
