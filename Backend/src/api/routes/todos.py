from fastapi import APIRouter, HTTPException
from src.db.mongodb import get_database
from src.models.todo import Todo, TodoCreate
from datetime import timezone
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Todo)
async def create_todo(todo: TodoCreate):
    db = await get_database()
    todo_dict = todo.model_dump()
    todo_dict["created_at"] = timezone.utc
    result = await db.todos.insert_one(todo_dict)
    todo_dict["_id"] = str(result.inserted_id)
    return Todo(**todo_dict)

@router.delete("/{todo_id}")
async def delete_todo(todo_id: str):
    db = await get_database()
    result = await db.todos.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

@router.get("/", response_model=list[Todo])
async def list_todos():
    db = await get_database()
    todos = []
    cursor = db.todos.find()
    async for todo in cursor:
        todo["_id"] = str(todo["_id"])
        todos.append(Todo(**todo))
    return todos 