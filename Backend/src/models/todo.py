from datetime import datetime
from pydantic import BaseModel, Field

class TodoCreate(BaseModel):
    title: str
    description: str | None = None

class Todo(TodoCreate):
    id: str = Field(default_factory=str, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow) 