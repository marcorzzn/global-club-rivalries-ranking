import json
with open('data/priority_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

for i in range(35, 50):
    print(f"{i+1}. {queue[i]['rivalry_id']}")
