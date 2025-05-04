from fastapi import HTTPException
from typing import List
from datetime import date

from app.models import notes_store
from app.schemas import NoteCreate, NoteUpdate, NoteInDB

class NoteService:
    @staticmethod
    def list_notes() -> List[NoteInDB]:
        return notes_store

    @staticmethod
    def get_note(note_id: int) -> NoteInDB:
        for note in notes_store:
            if note.id == note_id:
                return note
        raise HTTPException(status_code=404, detail="Note not found")

    @staticmethod
    def create_note(data: NoteCreate) -> NoteInDB:
        new_id = max((n.id for n in notes_store), default=0) + 1
        note = NoteInDB(id=new_id, **data.dict())
        notes_store.append(note)
        return note

    @staticmethod
    def update_note(note_id: int, data: NoteCreate) -> NoteInDB:
        note = NoteService.get_note(note_id)
        note.title = data.title
        note.content = data.content
        note.due_date = data.due_date
        return note

    @staticmethod
    def patch_note(note_id: int, data: NoteUpdate) -> NoteInDB:
        note = NoteService.get_note(note_id)
        update_data = data.dict(exclude_unset=True)
        for key, val in update_data.items():
            setattr(note, key, val)
        return note

    @staticmethod
    def delete_note(note_id: int) -> None:
        note = NoteService.get_note(note_id)
        notes_store.remove(note)
