import json
import re

ranking = json.load(open('data/rivalries_ranking.json', encoding='utf-8'))
excluded = json.load(open('data/ranking_excluded.json', encoding='utf-8'))

new_ranking = []
removed = 0
for r in ranking:
    team1, team2 = r['team1'], r['team2']
    p = r['p_raw']
    
    is_bad = False
    reason = ''
    
    if '-->' in team1 or '-->' in team2:
        is_bad = True; reason = 'HTML comment in team name'
    elif '<br>' in team1 or '<br>' in team2 or "'''" in team1 or "'''" in team2:
        is_bad = True; reason = 'HTML/Wiki markup in team name'
    elif 'Army' in team1 and 'Navy' in team1:
        is_bad = True; reason = 'College soccer'
    elif p > 2000:
        is_bad = True; reason = 'p_raw unrealistically high (>2000)'
    elif p == 200 and r['league'] == 'Premier League':
        # Too many generic '200' from 'over 200 London derbies'
        is_bad = True; reason = 'Generic 200 pattern for London derbies'
        
    if r['name_en'] == 'Manchester United F.C. 8–2 Arsenal F.C.' or r['name_en'] == 'Manchester United F.C. 1–6 Manchester City F.C.':
        is_bad = True; reason = 'Specific match'
        
    if 'Cup' in team1 or 'Cup' in team2:
        if 'Army' in team1 or 'Navy' in team1:
            is_bad = True; reason = 'Cup/Trophy page instead of rivalry'
            
    if 'Jing' == team1 and 'Hu' == team2:
        is_bad = True; reason = 'City names instead of clubs'
        
    if 'Manchester United' in r['name_en'] and 'Arsenal' in r['name_en'] and p == 49:
        is_bad = True; reason = 'Arsenal 49 unbeaten streak'

    if is_bad:
        excluded.append({'title': r['name_en'], 'reason': f'False positive: {reason}'})
        print(f"Removed: {team1} vs {team2} | {reason}")
        removed += 1
    else:
        new_ranking.append(r)

# Deduplicate by teams
seen_teams = {}
final_ranking = []
for r in new_ranking:
    t1, t2 = sorted([r['team1'].lower(), r['team2'].lower()])
    pair = f"{t1}-{t2}"
    if pair not in seen_teams:
        seen_teams[pair] = True
        final_ranking.append(r)
    else:
        print(f"Removed duplicate: {r['team1']} vs {r['team2']}")
        removed += 1
        excluded.append({'title': r['name_en'], 'reason': 'Duplicate team pairing'})

with open('data/rivalries_ranking.json', 'w', encoding='utf-8') as f:
    json.dump(final_ranking, f, ensure_ascii=False, indent=2)
with open('data/ranking_excluded.json', 'w', encoding='utf-8') as f:
    json.dump(excluded, f, ensure_ascii=False, indent=2)

print(f'\nTotal removed: {removed}')
