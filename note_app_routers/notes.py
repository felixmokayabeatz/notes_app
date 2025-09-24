from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud, database
from auth import get_current_user
import models

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=schemas.NoteOut)
def create_note(note: schemas.NoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_note(db, note, current_user.id)

@router.get("/", response_model=list[schemas.NoteOut])
def list_notes(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_notes(db, current_user.id)
