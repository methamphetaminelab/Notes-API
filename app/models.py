from typing import List
from app.schemas import NoteInDB

notes_store: List[NoteInDB] = []

from app.models import notes_store
from app.schemas import NoteCreate, NoteUpdate, NoteInDB
from fastapi import HTTPException

class NoteService:
    @staticmethod
    def list_notes():
        return notes_store

    @staticmethod
    def get_note(note_id: int) -> NoteInDB:
        for note in notes_store:
            if note.id == note_id:
                return note
        raise HTTPException(status_code=404, detail="Note not found")

    @staticmethod
    def create_note(data: NoteCreate) -> NoteInDB:
        new_id = max([n.id for n in notes_store], default=0) + 1
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
        for k, v in update_data.items():
            setattr(note, k, v)
        return note

    @staticmethod
    def delete_note(note_id: int):
        note = NoteService.get_note(note_id)
        notes_store.remove(note)
        return