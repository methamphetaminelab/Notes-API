from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[date]

    @validator("due_date")
    def check_due_date(cls, v):
        if v and v < date.today():
            raise ValueError("due_date must be today or in the future")
        return v

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[date]

    @validator("due_date")
    def check_update_due_date(cls, v):
        if v and v < date.today():
            raise ValueError("due_date must be today or in the future")
        return v

class NoteInDB(NoteBase):
    id: int

class NoteOut(NoteInDB):
    pass