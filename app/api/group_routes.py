from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.group_schema import Group, Participant
from pydantic import BaseModel
import uuid
from typing import List, Optional
from app.config import settings

router = APIRouter()

# --- Pydantic Schemas ---
class ParticipantCreate(BaseModel):
    name: str
    email: str

class ParticipantResponse(BaseModel):
    id: str
    name: str
    email: str
    survey_link: Optional[str] = None
    status: Optional[str] = None 
    # Note: DB has 'has_responded' (int), not status string, but our API was returning status="pending" 
    # in add_participant. But for the list view, we need to map correctly.
    # Actually, let's align with the DB model for read.
    has_responded: int

    class Config:
        from_attributes = True

class GroupCreate(BaseModel):
    name: str
    creator_email: str
    start_city: str
    max_budget: float
    travel_month: str
    duration: int
    group_size: int

class GroupResponse(GroupCreate):
    id: str
    status: str
    participants: List[ParticipantResponse] = []

    class Config:
        from_attributes = True

# --- Endpoints ---

@router.post("/groups", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(group_in: GroupCreate, db: Session = Depends(get_db)):
    # Generate UUID
    new_id = str(uuid.uuid4())
    
    db_group = Group(
        id=new_id,
        name=group_in.name,
        creator_email=group_in.creator_email,
        start_city=group_in.start_city,
        max_budget=group_in.max_budget,
        travel_month=group_in.travel_month,
        duration=group_in.duration,
        group_size=group_in.group_size,
        status="collecting"
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.post("/groups/{group_id}/participants", status_code=status.HTTP_201_CREATED)
def add_participant(group_id: str, participant_in: ParticipantCreate, db: Session = Depends(get_db)):
    import traceback
    try:
        print(f"DEBUG: Adding participant to {group_id}")
        # Verify group exists
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            print("DEBUG: Group not found")
            raise HTTPException(status_code=404, detail="Group not found")
        print(f"DEBUG: Group found: {group.name}")
        
        # Check duplicate email in group
        existing = db.query(Participant).filter(
            Participant.group_id == group_id, 
            Participant.email == participant_in.email
        ).first()
        
        if existing:
            return {"message": "Participant already exists", "participant_id": existing.id}

        new_p_id = str(uuid.uuid4())
        
        # dynamic_link = f"{settings.GOOGLE_FORM_LINK}&entry.12345={group_id}" 
        # For now, just sending the raw link or appending ID if we knew the field ID
        # Let's assume user just sends the main link, and we rely on manual grouping for MVP 
        # OR we append ?gid={group_id} just in case they added hidden fields
        
        final_link = f"{settings.GOOGLE_FORM_LINK}&entry.123456789={group_id}" # Example field ID, replace if known
        
        new_participant = Participant(
            id=new_p_id,
            group_id=group_id,
            name=participant_in.name,
            email=participant_in.email,
            survey_link=settings.GOOGLE_FORM_LINK, 
        )
        print("DEBUG: Object created, adding to DB session")
        db.add(new_participant)
        
        db.commit()
        print("DEBUG: Commit successful")
        
        # Trigger Email Invite
        invite_res = {"status": "skipped"}
        try:
            from app.services.email_service import EmailService
            # In a real app, use BackgroundTasks for this
            sent = EmailService.send_invite(
                to_email=new_participant.email, 
                group_name=group.name, 
                survey_link=new_participant.survey_link
            )
            invite_res = {"status": "sent" if sent else "failed"}
        except Exception as e:
            print(f"EMAIL ERROR: {e}")
            invite_res = {"status": "failed", "error": str(e)}
        
        return {
            "message": "Participant added", 
            "participant_id": new_p_id, 
            "link": new_participant.survey_link, 
            "invite_status": invite_res
        }
    except HTTPException:
        raise
    except Exception as e:
        print("CRITICAL ERROR IN ADD_PARTICIPANT:")
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Crash: {str(e)}")

@router.get("/groups/{group_id}", response_model=GroupResponse)
def get_group(group_id: str, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

# Phase 5: Hybrid Recommendation Endpoint
@router.post("/groups/{group_id}/recommendations")
def recommend_for_group(group_id: str, db: Session = Depends(get_db)):
    from app.services.recommendation import RecommendationService
    from app.models.place import Place
    import json
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
        
    # 1. Aggregate Preferences
    # Combine all participant preferences into one big text blob for TF-IDF
    aggregated_text = []
    total_budget_pref = 0
    count = 0
    
    for p in group.participants:
        if p.preferences: # JSON string
            try:
                # Assuming simple list of strings or dict
                # MVP: Just taking raw values and dumping to text
                data = json.loads(p.preferences) 
                # Improve this parsing based on actual form structure later
                aggregated_text.append(" ".join(str(v) for v in data))
            except:
                pass
        count += 1
        
    combined_query = " ".join(aggregated_text)
    
    # 2. Filter Candidates (Hard Constraints)
    # Use Group Max Budget
    service = RecommendationService(db)
    candidates = service.filter_places(max_budget=group.max_budget)
    
    # 3. Rank Candidates (Hybrid Scoring)
    group_prefs = {
        "travel_month": group.travel_month,
        "start_city": group.start_city,
        "combined_text": combined_query
    }
    ranked_places = service.rank_places(candidates, group_prefs=group_prefs)
    
    # Return top 5
    return ranked_places[:5]

@router.post("/groups/{group_id}/itinerary")
def generate_trip_plan(group_id: str, payload: dict, db: Session = Depends(get_db)):
    """
    Payload: { "destination": "Goa", "weather_summary": "Sunny..." }
    """
    from app.services.itinerary_service import ItineraryService
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
         raise HTTPException(status_code=404, detail="Group not found")
         
    # Aggregate preferences again or pass from frontend? 
    # Let's simple-aggregate here
    aggr_prefs = []
    for p in group.participants:
        if p.preferences:
            aggr_prefs.append(str(p.preferences))
    context = " ".join(aggr_prefs)
    
    destination = payload.get("destination")
    weather = payload.get("weather_summary", "Not available")
    
    plan = ItineraryService.generate_itinerary(
        destination_name=destination,
        duration=group.duration,
        group_context=context,
        weather_summary=weather
    )
    
    return plan
