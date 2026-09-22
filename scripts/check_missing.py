import json

with open('data/rivalries_encyclopaedia.json', encoding='utf-8') as f:
    enc = json.load(f)

search_terms = ['north west', 'paulista', 'fla-flu', 'fla_flu', 'gran derbi', 'el gran']

print("=== DERBIES SEARCH IN ENCYCLOPAEDIA ===")
for e in enc:
    name = e.get('name_en', '').lower()
    eid = e.get('id', '').lower()
    if any(t in name or t in eid for t in search_terms):
        print(f"  FOUND: id={e['id']} | name_en={e['name_en']}")

print(f"\nTotal enc entries: {len(enc)}")

# Also test noise filter on these titles
import sys, os
sys.path.insert(0, 'scripts')
from utils import is_noise_page

test_titles = [
    'North West derby (association football)',
    'Paulista Derby',
    'Fla-Flu',
    'El Gran Derbi',
    'Liverpool F.C.–Manchester United F.C. rivalry',
]
print("\n=== NOISE FILTER TEST ===")
for t in test_titles:
    result = is_noise_page(t)
    print(f"  {'NOISE' if result else 'OK   '}: {t}")
