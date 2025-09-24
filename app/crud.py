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


import uuid

def update_note(db: Session, note_id: int, note_data: schemas.NoteUpdate, user_id: int):
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == user_id
    ).first()
    if not note:
        return None

    # Update only provided fields
    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content

    # Handle sharing logic
    if note_data.shared is not None:
        if note_data.shared:
            note.shared = True
            if not note.share_id:  # generate share_id if not already present
                note.share_id = str(uuid.uuid4())
        else:
            note.shared = False
            note.share_id = None  # remove share_id if unsharing

    db.commit()
    db.refresh(note)
    return note



def get_note_by_share_id(db: Session, share_id: str):
    return db.query(models.Note).filter(models.Note.share_id == share_id, models.Note.shared == True).first()


def get_note_by_id(db: Session, note_id: int, user_id: int):
    return db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == user_id
    ).first()
