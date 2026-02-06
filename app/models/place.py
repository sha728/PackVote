from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.database import Base

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    state = Column(String(255), index=True)
    description = Column(Text)
    url = Column(String(500))
    
    # For constraints/filtering
    min_budget = Column(Float, nullable=True) 
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # For AI/Recommendation
    embedding = Column(JSON, nullable=True)
    weather_cache = Column(JSON, nullable=True)
