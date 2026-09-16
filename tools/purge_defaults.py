import json
import csv

def run():
    print("Purging unsourced values from rivalries...")
    with open('data/rivalries.json', 'r', encoding='utf-8') as f:
        rivs = json.load(f)
        
    audit_log = []
    purged_counts = {'h2h': 0, 'h_dom': 0, 'h_cont': 0, 'h_club': 0, 'i_soc': 0, 'i_name': 0, 'stadium': 0, 'attendance': 0}
    total_fields = 0
    preserved = 0
    
    def purge_metric(r, r_id, field, metric_obj, subfields):
        nonlocal total_fields, preserved
        has_val = False
        for sf in subfields:
            if metric_obj.get(sf) is not None:
                has_val = True
                
        if has_val:
            total_fields += 1
            source = metric_obj.get('source')
            if not source:
                for sf in subfields:
                    old_val = metric_obj.get(sf)
                    if old_val is not None:
                        metric_obj[sf] = None
                        audit_log.append({
                            'rivalry_id': r_id, 'field': f"{field}.{sf}" if len(subfields)>1 else field,
                            'old_value': old_val, 'new_value': 'null', 'reason': 'missing source'
                        })
                purged_counts[field] += 1
            else:
                preserved += 1
                
    for r in rivs:
        r_id = r['rivalry_id']
        purge_metric(r, r_id, 'h2h', r['h2h'], ['total', 'w_a', 'd', 'w_b'])
        purge_metric(r, r_id, 'stadium', r['stadium'], ['a', 'b'])
        purge_metric(r, r_id, 'h_club', r['h_club'], ['a', 'b'])
        purge_metric(r, r_id, 'h_dom', r['h_dom'], ['value'])
        purge_metric(r, r_id, 'h_cont', r['h_cont'], ['value'])
        purge_metric(r, r_id, 'i_soc', r['i_soc'], ['value'])
        purge_metric(r, r_id, 'i_name', r['i_name'], ['value'])
        purge_metric(r, r_id, 'attendance', r['attendance'], ['value'])

    with open('data/rivalries.json', 'w', encoding='utf-8') as f:
        json.dump(rivs, f, indent=2)
        
    with open('purge_audit.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['rivalry_id', 'field', 'old_value', 'new_value', 'reason'])
        writer.writeheader()
        writer.writerows(audit_log)
        
    print(f"\nTotal fields scanned: {total_fields}")
    nullified = sum(purged_counts.values())
    print(f"Values nullified: {nullified}")
    for k, v in purged_counts.items():
        if v > 0:
            print(f"  - {k}: {v}")
    print(f"Values preserved: {preserved}")

if __name__ == '__main__':
    run()
