from sqlalchemy import Column, Integer, String, ForeignKey, Boolean,Text
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    notes = relationship("Note", back_populates="owner")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    shared = Column(Boolean, default=False)
    share_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    owner = relationship("User", back_populates="notes")


from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String, unique=True, nullable=False)
    owner = Column(String, default="felix")
    created_at = Column(DateTime, default=datetime.utcnow)
