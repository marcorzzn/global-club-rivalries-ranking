import json
import os
import refresh_logos as rl

def main():
    print("=== fetch_new_logos.py ===")
    
    with open("data/rivalries_ranking.json", encoding="utf-8") as f:
        ranking = json.load(f)
        
    with open("data/logos.json", encoding="utf-8") as f:
        logos = json.load(f)
        
    all_teams = sorted({r["team1"] for r in ranking} | {r["team2"] for r in ranking})
    new_teams = [t for t in all_teams if t not in logos or not logos[t]]
    
    print(f"Total teams in ranking: {len(all_teams)}")
    print(f"New teams to fetch logos for: {len(new_teams)}")
    
    ok = 0
    rejected = 0
    missing = 0
    
    extra_aliases = {
        "Aberdeen": "Aberdeen F.C.",
        "Blackpool": "Blackpool F.C.",
        "Guadalajara": "C.D. Guadalajara",
        "Hanoi FC": "Hanoi FC",
        "Maccabi Tel Aviv": "Maccabi Tel Aviv F.C.",
        "Montreal Impact": "CF Montréal",
        "Nacional": "Club Nacional de Football",
        "Osijek": "NK Osijek",
        "Rijeka": "HNK Rijeka",
        "Fenerbahçe  (football)": "Fenerbahçe S.K. (football)",
        "Preston North End": "Preston North End F.C."
    }
    
    for name in new_teams:
        wiki_title = extra_aliases.get(name, rl.KNOWN_ALIASES.get(name, name))
        url, detail = rl.get_logo_from_wikitext(wiki_title)
        
        if url:
            logos[name] = url
            print(f"  [OK] {name:35} | {detail}")
            ok += 1
        else:
            if "SCARTATO" in detail:
                logos[name] = None
                print(f"  [NO] {name:35} | {detail}")
                rejected += 1
            else:
                logos[name] = None
                print(f"  [--] {name:35} | {detail}")
                missing += 1
                
    print(f"\n{'='*50}")
    print(f"OK (logo wikitext):         {ok}")
    print(f"Scartati (non-logo):        {rejected}")
    print(f"Mancanti (pagina assente):  {missing}")
    
    with open("data/logos.json", "w", encoding="utf-8") as f:
        json.dump(logos, f, indent=2, ensure_ascii=False)
        
    still_missing = [t for t in all_teams if not logos.get(t)]
    with open("fetch_logos_missing.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(still_missing))
        
    print("Logos updated successfully.")
    
if __name__ == "__main__":
    main()
