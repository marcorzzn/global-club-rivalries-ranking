import json
with open('data/rivalries_ranking.json', encoding='utf-8') as f:
    data = json.load(f)
print(f"Total: {len(data)} entries\n")
for r in data:
    src = r.get('p_raw_source_detail', '')[:90]
    print(f"  {r['name_en'][:35]:35} p={r['p_raw']:4} first={r['first_year']} | {src}")
