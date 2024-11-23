from fastapi import HTTPException, UploadFile, File, Form
from src.db.mongodb import get_database
from src.utils.normalizer import DataNormalizer
import pandas as pd
import json
from datetime import datetime
from bson import ObjectId

async def create_project(
    project_name: str = Form(...),
    csv_file: UploadFile = File(...),
    url: str = Form(...)
):
    try:
        # Read CSV content
        df = pd.read_csv(csv_file.file)
        
        # Convert DataFrame to JSON and normalize keys
        json_data = json.loads(df.to_json(orient='records'))
        normalized_data = DataNormalizer.normalize_keys(json_data)
        
        # Create project document
        db = await get_database()
        project_data = {
            "project_name": project_name,
            "url": url,
            "vulnerabilities": normalized_data,
            "created_at": datetime.utcnow()
        }
        
        result = await db.projects.insert_one(project_data)
        
        return {
            "message": "Project created successfully",
            "project_id": str(result.inserted_id)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 

async def get_vulnerabilities(project_id: str):
    try:
        db = await get_database()
        
        # Convert string ID to ObjectId
        project = await db.projects.find_one({"_id": ObjectId(project_id)})
        
        if not project:
            return {
                "status": False,
                "message": "Project not found"
            }, 404
            
        return {
            "project_name": project["project_name"],
            "vulnerabilities": project["vulnerabilities"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
#def get_project_data()