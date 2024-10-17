from fastapi import APIRouter, Depends, HTTPException
from .models import Session, UpdateSession
from deps.auth.auth import get_current_user
from uuid import uuid4
from app.db import db
from datetime import datetime, timezone


# nest sessions in the database like:
'''
{
    recurring: [recurring_session_object],
    schedule: [schedule_session_object],
    session: [session_object]
}
'''
router = APIRouter()


@router.post("", status_code=201, description="Create session")
async def create_session(session: Session, user=Depends(get_current_user)):
    id = str(uuid4())
    session_dict = session.model_dump(exclude_none=True)
    session_dict["_id"] = id
    session_dict["user"] = user["_id"]
    db["sessions"].insert_one(session_dict)
    session_dict["id"] = session_dict.pop("_id")
    return session_dict


@router.get("", status_code=200)
async def get_sessions(user=Depends(get_current_user)):
    sessions = list(db["sessions"].find({"user": user["_id"]}))
    for session in sessions:
        session["id"] = session.pop("_id")
    print(sessions)
    return sessions


@router.get("/active_sessions", status_code=200)
async def get_active_sessions():
    sessions = db["sessions"].find({"end_time": {"$gte": datetime.now(tz=timezone.utc)}})
    if sessions:
        sessions = list(sessions)
        for i in sessions:
            if i["block_lists"]:
                block_lists = db["block_lists"].find({"_id": {"$in": i["block_lists"]}})
                if block_lists:
                    block_lists = list(block_lists)
                    for block_list in block_lists:
                        i["block_lists"] = block_list["entries"]
            i["id"] = i.pop("_id")
        return sessions


@router.get("/{id}", status_code=200)
async def get_single_session(id: str, user=Depends(get_current_user)):
    session = db["sessions"].find_one({"_id": id})
    if session:
        session["id"] = session.pop("_id")
        return session
    raise HTTPException(status_code=400, detail="Session not found.")


@router.patch("/{id}", status_code=200, dependencies=[Depends(get_current_user)])
async def update_session(id: str, data: UpdateSession):
    data = data.model_dump(exclude_none=True)
    db["sessions"].update_one({"_id": id}, {"$set": data})
    return {"message": "Session updated successfully."}


@router.delete("/{id}", status_code=200, dependencies=[Depends(get_current_user)])
async def delete_session(id: str):
    session = db["sessions"].find_one_and_delete({"_id": id})
    if session:
        return f"{session['name']} has been deleted successfully"
    raise HTTPException(status_code=400, detail="Session with this ID does not exist.")
