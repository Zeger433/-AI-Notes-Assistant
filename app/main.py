from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Base, Note, User, NoteShare
from typing import List
from app.database import SessionLocal, engine, get_db
from app.models import Base, Note, User
from app.schemas import (
    NoteCreate,
    NoteResponse,
    UserCreate,
    UserResponse,
    UserLogin,
    NoteShareCreate,
)
from app.security import hash_password, verify_password
from app.auth import create_access_token, get_current_user
from app.models import User
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import AnalyzeRequest
from app.ai import analyze_note
from app.ai import analyze_note
from app.agent import run_agent
from app.schemas import AssistantRequest
import json
from app.models import Base, Note, User, NoteShare


app = FastAPI()

from app.agent import chat



@app.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(db_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/")
def home():
    return {"message": "Notes API"}




@app.get("/notes", response_model=List[NoteResponse])
def get_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notes = (
        db.query(Note)
        .outerjoin(
            NoteShare,
            Note.id == NoteShare.note_id
        )
        .filter(
            (Note.user_id == current_user.id)
            |
            (NoteShare.user_id == current_user.id)
        )
        .all()
    )

    return notes

@app.post("/notes", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ai_result = analyze_note(note.content)

    new_note = Note(
        title=note.title,
        content=note.content,
        summary=ai_result["summary"],
        category=ai_result["category"],
        tags=", ".join(ai_result["tags"]),
        user_id=current_user.id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


# @app.get("/ai/test")
# def test_ai():
#     response = ask_ai("Say hello, nice to meet you in one sentence.")
#     return {"response": response}
@app.get("/assistant/test")
def assistant_test():
    return {
        "response": chat("Say hello in one sentence.")
    }



@app.post("/ai/analyze")
def analyze_note_endpoint(request: AnalyzeRequest):
    return analyze_note(request.content)



@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    updated_note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    
):
    note = db.query(Note).filter(
    Note.id == note_id,
    Note.user_id == current_user.id
).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = updated_note.title
    note.content = updated_note.content

    db.commit()
    db.refresh(note)

    return note    


@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
    Note.id == note_id,
    Note.user_id == current_user.id
).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}   


@app.post("/notes/{note_id}/share")
def share_note(
    note_id: int,
    share_data: NoteShareCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Check note ownership
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()


    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found or you are not the owner"
        )


    # Find user to share with
    shared_user = db.query(User).filter(
        User.email == share_data.email
    ).first()


    if shared_user is None:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )


    # Prevent sharing with yourself
    if shared_user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot share a note with yourself"
        )


    # Check existing share
    existing_share = db.query(NoteShare).filter(
        NoteShare.note_id == note_id,
        NoteShare.user_id == shared_user.id
    ).first()


    if existing_share:
        raise HTTPException(
            status_code=400,
            detail="Note already shared with this user"
        )


    # Create share record
    new_share = NoteShare(
        note_id=note.id,
        user_id=shared_user.id,
        permission=share_data.permission
    )


    db.add(new_share)
    db.commit()
    db.refresh(new_share)


    return {
        "message": "Note shared successfully",
        "note_id": note_id,
        "shared_with": share_data.email,
        "permission": share_data.permission
    }


@app.post("/assistant")
def assistant(
    request: AssistantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response = run_agent(
        db=db,
        user_id=current_user.id,
        prompt=request.prompt,
    )

    return {
        "response": response
    }