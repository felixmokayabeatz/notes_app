from pydantic import BaseModel, EmailStr
from typing import List, Optional

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
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str
    content: str
    shared: Optional[bool] = False

class NoteOut(NoteBase):
    id: int
    owner_id: int
    shared: bool
    share_id: str

    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
