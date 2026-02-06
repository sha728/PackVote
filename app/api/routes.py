from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.recommendation import RecommendationService
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class PlaceResponse(BaseModel):
    name: str
    state: Optional[str]
    description: Optional[str]
    url: Optional[str]
    min_budget: Optional[float]

    class Config:
        from_attributes = True

@router.get("/recommendations", response_model=List[PlaceResponse])
def get_recommendations(
    max_budget: Optional[float] = Query(None, description="Maximum budget per person"),
    preferred_states: Optional[List[str]] = Query(None, description="List of preferred states"),
    query: Optional[str] = Query(None, description="Free text query for similarity matching"),
    db: Session = Depends(get_db)
):
    service = RecommendationService(db)
    
    # 1. Filter
    candidates = service.filter_places(max_budget=max_budget, preferred_states=preferred_states)
    
    # 2. Rank (if query provided)
    if query:
        # For single user query mode, treating query as "group_preferences"
        candidates = service.rank_places(candidates, group_preferences=query)
        
    return candidates

from app.services.ai_itinerary import ItineraryService

class ItineraryRequest(BaseModel):
    place_name: str
    duration: int
    preferences: str

@router.post("/itinerary")
async def create_itinerary(request: ItineraryRequest):
    service = ItineraryService()
    itinerary = await service.generate_itinerary(request.place_name, request.duration, request.preferences)
    return {"itinerary": itinerary}
