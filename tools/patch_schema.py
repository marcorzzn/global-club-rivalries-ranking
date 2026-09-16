import json

def run():
    with open('data/rivalry_schema.json', 'r', encoding='utf-8') as f:
        schema = json.load(f)
        
    schema['properties']['match_context'] = {
        "type": "object",
        "properties": {
            "continental_finals": {"$ref": "#/definitions/sourced_metric_integer"},
            "top5_league": {"$ref": "#/definitions/sourced_metric_integer"},
            "top10_league": {"$ref": "#/definitions/sourced_metric_integer"},
            "national_cups": {"$ref": "#/definitions/sourced_metric_integer"},
            "state_regional": {"$ref": "#/definitions/sourced_metric_integer"}
        }
    }
    
    with open('data/rivalry_schema.json', 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)

if __name__ == '__main__':
    run()
