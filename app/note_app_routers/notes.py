from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.auth import get_current_user
from app import models

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=schemas.NoteOut)
def create_note(note: schemas.NoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_note(db, note, current_user.id)

@router.get("/", response_model=list[schemas.NoteOut])
def list_notes(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_notes(db, current_user.id)


@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note_endpoint(
    note_id: int,
    note: schemas.NoteUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    updated_note = crud.update_note(db, note_id, note, current_user.id)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found or not yours")
    return updated_note

@router.get("/shared/{share_id}", response_model=schemas.NoteOut)
def get_shared_note(share_id: str, db: Session = Depends(database.get_db)):
    note = crud.get_note_by_share_id(db, share_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or not shared")
    return note


