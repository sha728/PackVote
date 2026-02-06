import json
import re
from pathlib import Path
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_FILE = os.path.join(BASE_DIR, "data", "raw", "holidify_india_places_all.json")

CLEAN_FILE = "data/processed/holidify_india_places_clean.json"

def clean_name(name):
    # Remove leading numbering like "1. "
    return re.sub(r"^\d+\.\s*", "", name).strip()

def clean_description(desc):
    if not desc:
        return "Popular tourist destination in India"
    return "Popular tourist destination in India"

def clean_best_time(best_time):
    if not best_time:
        return None
    return best_time.replace("Read More", "").strip()

def clean_dataset():
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []

    for item in data:
        cleaned.append({
            "name": clean_name(item.get("name")),
            "state": None,  # will be enriched later
            "best_time": clean_best_time(item.get("best_time")),
            "description": clean_description(item.get("description")),
            "url": item.get("url")
        })

    Path(CLEAN_FILE).parent.mkdir(parents=True, exist_ok=True)

    with open(CLEAN_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Cleaned dataset saved to {CLEAN_FILE}")
    print(f"Total destinations cleaned: {len(cleaned)}")

if __name__ == "__main__":
    clean_dataset()
