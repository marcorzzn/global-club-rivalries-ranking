import json

corrections = {
    "clube-atletico-mineiro--cruzeiro-ec": 388,
    "cr-flamengo--cr-vasco-da-gama": 350,
    "ec-bahia--ec-vitoria": 370,
    "club-cerro-porteno--club-olimpia": 380,
    "sc-corinthians--se-palmeiras": 320
}

def run():
    with open('data/rivalries.json', 'r', encoding='utf-8') as f:
        rivs = json.load(f)
        
    for r in rivs:
        rid = r['rivalry_id']
        if rid in corrections:
            new_tot = corrections[rid]
            old_tot = r['h2h']['total']['value'] if isinstance(r['h2h']['total'], dict) else r['h2h']['total']
            if old_tot is None: continue
            
            w_a = r['h2h']['w_a']['value'] if isinstance(r['h2h']['w_a'], dict) else r['h2h']['w_a']
            d = r['h2h']['d']['value'] if isinstance(r['h2h']['d'], dict) else r['h2h']['d']
            w_b = r['h2h']['w_b']['value'] if isinstance(r['h2h']['w_b'], dict) else r['h2h']['w_b']
            
            factor = new_tot / old_tot
            
            new_wa = int(round(w_a * factor))
            new_wb = int(round(w_b * factor))
            new_d = new_tot - new_wa - new_wb  # Ensure sum is exact
            
            if isinstance(r['h2h']['total'], dict):
                r['h2h']['total']['value'] = new_tot
                r['h2h']['w_a']['value'] = new_wa
                r['h2h']['d']['value'] = new_d
                r['h2h']['w_b']['value'] = new_wb
                r['h2h']['total']['source'] = "Parziali stimati proporzionalmente dopo esclusione amichevoli"
            else:
                r['h2h']['total'] = new_tot
                r['h2h']['w_a'] = new_wa
                r['h2h']['d'] = new_d
                r['h2h']['w_b'] = new_wb
                r['h2h']['source'] = "Parziali stimati proporzionalmente dopo esclusione amichevoli"
                
    with open('data/rivalries.json', 'w', encoding='utf-8') as f:
        json.dump(rivs, f, indent=2)
        
    print("Corrections applied successfully.")

if __name__ == '__main__':
    run()
