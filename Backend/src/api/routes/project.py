from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from src.db.mongodb import get_database
from src.models.todo import Todo, TodoCreate
from datetime import datetime
from bson import ObjectId
import pandas as pd
import json

router = APIRouter()

@router.post("/create")
async def create_project(
    project_name: str = Form(...),
    csv_file: UploadFile = File(...),
    url: str = Form(...)
):
    try:
        # Read CSV content
        df = pd.read_csv(csv_file.file)
        
        # Convert DataFrame to JSON
        json_data = json.loads(df.to_json(orient='records'))
        
        # Create project document
        db = await get_database()
        project_data = {
            "project_name": project_name,
            "url": url,
            "data": json_data,
            "created_at": datetime.utcnow()
        }
        
        result = await db.projects.insert_one(project_data)
        
        return {
            "message": "Project created successfully",
            "project_id": str(result.inserted_id)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 