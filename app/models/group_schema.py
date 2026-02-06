from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Group(Base):
    __tablename__ = "groups"

    id = Column(String, primary_key=True, index=True) # UUID via str for SQLite compatibility, or UUID for PG
    name = Column(String, index=True)
    creator_email = Column(String) # [NEW] Capture creator's email
    start_city = Column(String)
    max_budget = Column(Float)
    travel_month = Column(String)
    duration = Column(Integer)
    group_size = Column(Integer)
    status = Column(String, default="collecting") # 'collecting', 'ranking', 'done'
    
    participants = relationship("Participant", back_populates="group")

class Participant(Base):
    __tablename__ = "participants"

    id = Column(String, primary_key=True, index=True) # UUID
    group_id = Column(String, ForeignKey("groups.id"))
    name = Column(String)
    email = Column(String) # [MODIFIED] phone_number -> email
    survey_link = Column(String)
    has_responded = Column(Integer, default=0) # 0 or 1
    
    # Store raw answers or flattened vector
    preferences = Column(JSON, nullable=True) 

    group = relationship("Group", back_populates="participants")
