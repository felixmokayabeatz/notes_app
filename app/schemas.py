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

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    shared: Optional[bool] = None


class NoteOut(NoteBase):
    id: int
    owner_id: int
    shared: bool
    share_id: Optional[str] = None

    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
