import json

# Carichiamo i dati falsati per prendere le metriche qualitative base come fallback, 
# ma sovrascriviamo l'H2H e match_context per testare la V2 sui 6 veri.
with open('data/rivalries.json', 'r', encoding='utf-8') as f:
    rivs = json.load(f)

real_data = {
    'fc-barcelona--real-madrid': {'tot': 264, 'wa': 106, 'd': 52, 'wb': 106, 'mc_top5': 188, 'mc_nc': 65, 'mc_cf': 0},
    'ac-milan--fc-internazionale-milano': {'tot': 246, 'wa': 91, 'd': 71, 'wb': 84, 'mc_top5': 180, 'mc_nc': 40, 'mc_cf': 0},
    'ca-boca-juniors--ca-river-plate': {'tot': 266, 'wa': 88, 'd': 84, 'wb': 94, 'mc_top10': 214, 'mc_nc': 44, 'mc_cf': 2},
    'club-america--cruz-azul': {'tot': 206, 'wa': 74, 'd': 69, 'wb': 63, 'mc_top10': 170, 'mc_nc': 22, 'mc_cf': 0},
    'al-ahly-sc--zamalek-sc': {'tot': 137, 'wa': 62, 'd': 43, 'wb': 32, 'mc_top10': 100, 'mc_nc': 35, 'mc_cf': 2},
    'kaizer-chiefs--orlando-pirates': {'tot': 176, 'wa': 74, 'd': 54, 'wb': 48, 'mc_nc': 60, 'mc_sr': 116, 'mc_cf': 0}
}

test_rivs = []
for r in rivs:
    rid = r['rivalry_id']
    if rid in real_data:
        d = real_data[rid]
        r['h2h']['total'] = {'value': d['tot']}
        r['h2h']['w_a'] = {'value': d['wa']}
        r['h2h']['d'] = {'value': d['d']}
        r['h2h']['w_b'] = {'value': d['wb']}
        
        r['match_context'] = {
            'continental_finals': {'value': d.get('mc_cf', 0)},
            'top5_league': {'value': d.get('mc_top5', 0)},
            'top10_league': {'value': d.get('mc_top10', 0)},
            'national_cups': {'value': d.get('mc_nc', 0)},
            'state_regional': {'value': d.get('mc_sr', 0)}
        }
        test_rivs.append(r)

with open('data/test_real.json', 'w', encoding='utf-8') as f:
    json.dump(test_rivs, f, indent=2)

print('Creato file di test con i 6 veri.')
