from pydantic import BaseModel, EmailStr
from typing import List, Optional

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# Note schemas
class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
