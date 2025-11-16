import json
from datetime import datetime

STATS_FILE = "cache/stats.json"

def update_stats(model: str, tokens: int = 0):
    stats = {"sessions": 0, "models": {}, "last_used": ""}
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
    
    stats["sessions"] += 1
    stats["models"][model] = stats["models"].get(model, 0) + 1
    stats["last_used"] = datetime.now().isoformat()
    
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)
    
    return stats