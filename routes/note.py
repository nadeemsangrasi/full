from model.note import Note
from config.db import conn
from schemas.note import notes_entity
from typing import Union
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId

templates = Jinja2Templates(directory="templates")
note = APIRouter()
@note.get("/",response_class=HTMLResponse)
async def read_item(request:Request):
    docs = conn.notes.notes.find({})
    newDocs=notes_entity(docs)
    return templates.TemplateResponse("index.html",{"request":request,"newDocs":newDocs})

@note.post("/")
async def create_item(request:Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"]=True if formDict.get("important")=="on" else False 
    conn.notes.notes.insert_one(formDict)    
    if formDict:
        return {"message":"note added successfully"}
    else:
        return {"message":"error found"}

@note.get("/delete_note/{note_id}")
async def delete_note(note_id:str)->dict[str,str]:
    note = conn.notes.notes.find_one({"_id":ObjectId(note_id)})
    if note:
        conn.notes.notes.delete_one({"_id":note["_id"]})
        return {"message": "Note : '{}' deleted successfully.".format(note["title"])}
    else:
        return {"message": "note not found."}
 
    
@note.get("/edit_note/{note_id}")
async def update_note(note_id:str)->dict[str,str]:
    note = conn.notes.notes.find_one({"_id":ObjectId(note_id)})
    if note:
        conn.notes.notes.delete_one({"_id":note["_id"]})
        return {"message": "eidit your note"}
    else:
        return {"message":"note not found"}