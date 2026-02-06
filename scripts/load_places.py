import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Place, Group, Participant 

def load_places():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    input_file = os.path.join("data", "processed", "holidify_india_places_final.json")
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        places_data = json.load(f)

    print(f"Found {len(places_data)} places to load...")
    
    for item in places_data:
        # Check if exists
        exists = db.query(Place).filter(Place.name == item["name"]).first()
        if exists:
            continue
            
        new_place = Place(
            name=item["name"],
            state=item.get("state"),
            description=item.get("description"),
            url=item.get("url"),
            # Default values for now
            min_budget=1000.0, 
        )
        db.add(new_place)
    
    db.commit()
    print("Data loading complete!")
    db.close()

if __name__ == "__main__":
    load_places()
