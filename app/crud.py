from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash, verify_password, create_access_token

# User
def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Note
def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(title=note.title, content=note.content, owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes(db: Session, user_id: int):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()


# app/crud.py
def update_note(db: Session, note_id: int, note_data: schemas.NoteUpdate, user_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == user_id).first()
    if not note:
        return None
    note.title = note_data.title
    note.content = note_data.content
    note.shared = note_data.shared
    db.commit()
    db.refresh(note)
    return note

def get_note_by_share_id(db: Session, share_id: str):
    return db.query(models.Note).filter(models.Note.share_id == share_id, models.Note.shared == True).first()
