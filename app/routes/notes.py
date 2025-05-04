from fastapi import APIRouter, HTTPException
from app.schemas import NoteCreate, NoteUpdate, NoteOut
from app.services import NoteService
from fastapi.responses import Response

router = APIRouter()

@router.get("/", response_model=list[NoteOut])
async def list_notes():
    return NoteService.list_notes()

@router.get("/{note_id}", response_model=NoteOut)
async def get_note(note_id: int):
    return NoteService.get_note(note_id)

@router.post("/", response_model=NoteOut, status_code=201)
async def create_note(data: NoteCreate):
    return NoteService.create_note(data)

@router.put("/{note_id}", response_model=NoteOut)
async def update_note(note_id: int, data: NoteCreate):
    return NoteService.update_note(note_id, data)

@router.patch("/{note_id}", response_model=NoteOut)
async def patch_note(note_id: int, data: NoteUpdate):
    return NoteService.patch_note(note_id, data)

@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: int):
    NoteService.delete_note(note_id)
    return Response(status_code=204)

@router.head("/{note_id}")
async def head_note(note_id: int):
    _ = NoteService.get_note(note_id)
    return Response(status_code=200)

@router.options("/")
async def options_notes():
    return Response(headers={"Allow": "GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS"})