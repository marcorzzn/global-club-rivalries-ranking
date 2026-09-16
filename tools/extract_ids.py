import json

def run():
    with open('data/priority_queue.json', 'r', encoding='utf-8') as f:
        queue = json.load(f)
        
    print("Batch 003 (16-20):")
    for i in range(15, 20):
        print(f"{i+1}. {queue[i]['rivalry_id']}")
        
    print("\nBatch 004 (21-25):")
    for i in range(20, 25):
        print(f"{i+1}. {queue[i]['rivalry_id']}")
        
    print("\nBatch 005 (26-30):")
    for i in range(25, 30):
        print(f"{i+1}. {queue[i]['rivalry_id']}")

if __name__ == '__main__':
    run()
