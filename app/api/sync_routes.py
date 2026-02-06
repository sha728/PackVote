from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.sheet_sync import SheetSyncService

router = APIRouter()

@router.post("/sync/{group_id}")
def sync_group_data(group_id: str, db: Session = Depends(get_db)):
    service = SheetSyncService(db)
    service.sync_responses(group_id)
    return {"message": "Sync triggered"}
