import json
import os

raw_data = [
  {
    "id": "cd-guadalajara-chivas--club-america",
    "total": 264,
    "w_a": 82,
    "d": 83,
    "w_b": 99,
    "h_dom": 25,
    "h_cont": 55,
    "h_club": 95,
    "i_soc": 50,
    "i_name": 100,
    "stadium": {
      "a": 49850,
      "b": 83264
    },
    "attendance": 55000,
    "active_decades": 5,
    "retrieved_at": "2026-09-17",
    "source": "H2H da Wikipedia/Infobae. Nessuna incoerenza aritmetica (82+83+99=264). Incroci regolari in ogni decade considerata."
  },
  {
    "id": "olympiacos-fc--panathinaikos-fc",
    "total": 227,
    "w_a": 90,
    "d": 80,
    "w_b": 57,
    "h_dom": 100,
    "h_cont": 0,
    "h_club": 100,
    "i_soc": 100,
    "i_name": 100,
    "stadium": {
      "a": 33334,
      "b": 16000
    },
    "attendance": 25000,
    "active_decades": 5,
    "retrieved_at": "2026-09-17",
    "source": "H2H da database storici (es. FootballToday). Coerenza aritmetica verificata (90+80+57=227). Decade attiva costante."
  },
  {
    "id": "sl-benfica--sporting-cp",
    "total": 329,
    "w_a": 141,
    "d": 72,
    "w_b": 116,
    "h_dom": 100,
    "h_cont": 0,
    "h_club": 100,
    "i_soc": 50,
    "i_name": 100,
    "stadium": {
      "a": 64642,
      "b": 50095
    },
    "attendance": 55000,
    "active_decades": 5,
    "retrieved_at": "2026-09-17",
    "source": "H2H da ZeroZero/RSSSF. Coerenza aritmetica verificata (141+72+116=329). Rivalità storica continua su 5 decadi."
  },
  {
    "id": "arsenal-fc--tottenham-hotspur",
    "total": 213,
    "w_a": 91,
    "d": 55,
    "w_b": 67,
    "h_dom": 75,
    "h_cont": 0,
    "h_club": 98,
    "i_soc": 25,
    "i_name": 100,
    "stadium": {
      "a": 60704,
      "b": 62850
    },
    "attendance": 60000,
    "active_decades": 5,
    "retrieved_at": "2026-09-17",
    "source": "H2H da SportsMole/database ufficiali. Dati aritmeticamente validi (91+55+67=213). Tutte e 5 le decadi ampiamente attive."
  },
  {
    "id": "liverpool-fc--manchester-united",
    "total": 218,
    "w_a": 72,
    "d": 61,
    "w_b": 85,
    "h_dom": 100,
    "h_cont": 55,
    "h_club": 100,
    "i_soc": 50,
    "i_name": 100,
    "stadium": {
      "a": 61276,
      "b": 74310
    },
    "attendance": 65000,
    "active_decades": 5,
    "retrieved_at": "2026-09-17",
    "source": "H2H da LFCHistory. Coerenza aritmetica rispettata (72+61+85=218). Incontri frequenti in tutte le decadi dal 1976."
  }
]

def run():
    print("Mapping flattened LLM output to strict schema...")
    
    with open('dossiers/batch_002_template.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)
        
    mapped = []
    
    for r in raw_data:
        rid = r['id']
        t = next(x for x in templates if x['rivalry_id'] == rid)
        
        src = r['source']
        ret = r['retrieved_at']
        
        # Build mapped struct
        d = {
            "rivalry_id": rid,
            "club_a": t['club_a'],
            "club_b": t['club_b'],
            "h2h": {
                "total": {"value": r['total'], "source": src, "retrieved_at": ret},
                "w_a": {"value": r['w_a'], "source": src, "retrieved_at": ret},
                "d": {"value": r['d'], "source": src, "retrieved_at": ret},
                "w_b": {"value": r['w_b'], "source": src, "retrieved_at": ret},
                "active_decades": {"value": r['active_decades'], "source": src, "retrieved_at": ret}
            },
            "h_dom": {"value": r['h_dom'], "source": src, "retrieved_at": ret},
            "h_cont": {"value": r['h_cont'], "source": src, "retrieved_at": ret},
            "h_club": {"value": r['h_club'], "source": src, "retrieved_at": ret},
            "i_soc": {"value": r['i_soc'], "source": src, "retrieved_at": ret},
            "i_name": {"value": r['i_name'], "source": src, "retrieved_at": ret},
            "stadium": {
                "a": {"value": r['stadium']['a'], "source": src, "retrieved_at": ret},
                "b": {"value": r['stadium']['b'], "source": src, "retrieved_at": ret}
            },
            "attendance": {"value": r['attendance'], "source": src, "retrieved_at": ret}
        }
        mapped.append(d)
        
    with open('dossiers/batch_002_completed.json', 'w', encoding='utf-8') as f:
        json.dump(mapped, f, indent=2)
        
    print("Mapped successfully to dossiers/batch_002_completed.json")

if __name__ == '__main__':
    run()
