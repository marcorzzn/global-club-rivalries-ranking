import json
import os
import sys

def run(start_idx, end_idx, batch_num):
    print(f"Generating dossier template for Batch {batch_num}...")
    
    with open('data/priority_queue.json', 'r', encoding='utf-8') as f:
        queue = json.load(f)
        
    batch = queue[start_idx:end_idx]
    
    os.makedirs('dossiers', exist_ok=True)
    
    dossiers = []
    for r in batch:
        d = {
            "rivalry_id": r['rivalry_id'],
            "club_a": r['club_a_slug'],
            "club_b": r['club_b_slug'],
            "h2h": {
                "total": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
                "w_a": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
                "d": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
                "w_b": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
                "active_decades": {"value": None, "source": None, "retrieved_at": "2026-09-17"}
            },
            "h_dom": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
            "h_cont": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
            "h_club": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
            "i_soc": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
            "i_name": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
            "stadium": {
                "a": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
                "b": {"value": None, "source": None, "retrieved_at": "2026-09-17"}
            },
            "match_context": {
                "continental_finals": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
                "top5_league": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
                "top10_league": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
                "national_cups": {"value": None, "source": None, "retrieved_at": "2026-09-17"},
                "state_regional": {"value": None, "source": None, "retrieved_at": "2026-09-17"}
            },
            "attendance": {"value": None, "source": None, "retrieved_at": "2026-09-17"}
        }
        dossiers.append(d)
        
    out_file = f'dossiers/batch_{batch_num:03d}_template.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(dossiers, f, indent=2)
        
    print(f"Generated {out_file}")

if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
