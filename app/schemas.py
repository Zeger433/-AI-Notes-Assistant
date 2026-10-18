from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime



class NoteCreate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    summary: str | None = None
    category: str | None = None
    tags: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str   




class AnalyzeRequest(BaseModel):
    content: str    



class AssistantRequest(BaseModel):
    prompt: str    


class NoteShareCreate(BaseModel):
    email: str
    permission: str = "read"    