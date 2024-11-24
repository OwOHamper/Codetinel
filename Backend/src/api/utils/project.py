import traceback
from fastapi import HTTPException, UploadFile, File, Form, BackgroundTasks
from src.db.mongodb import get_database
from src.utils.normalizer import normalize_csv
import pandas as pd
import json
from datetime import timezone, datetime
from bson import ObjectId
from src.AI.index.indexing import index_repository
from bson.errors import InvalidId

async def create_project(
    project_name: str = Form(...),
    csv_file: UploadFile = File(...),
    url: str = Form(...),
    deployment_url: str = Form(...), 
    background_tasks: BackgroundTasks = None,
       
):
    try:
        # Read CSV content
        df = pd.read_csv(csv_file.file)
        
        # Convert DataFrame to JSON and normalize keys
        json_data = json.loads(df.to_json(orient='records'))
        normalized_data = normalize_csv(json_data)
        
        # Create project document
        db = await get_database()
        project_data = {
            "project_name": project_name,
            "url": url,
            "deployment_url": deployment_url,
            "vulnerabilities": normalized_data,
            "created_at": datetime.now(tz=timezone.utc),
            "indexing_status": "pending"
        }
        
        result = await db.projects.insert_one(project_data)
        project_id = str(result.inserted_id)
        
        # Add background task for indexing
        if background_tasks:
            background_tasks.add_task(
                index_repository,
                project_id=project_id,
                repo_url=url
            )
        
        return {
            "message": "Project created successfully, indexing started",
            "project_id": project_id
        }
        
    except Exception as e:
        print(traceback.format_exc())
        
        raise HTTPException(status_code=400, detail=str(e)) 

async def delete_project(project_id: str):
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(project_id):
            raise HTTPException(status_code=400, detail="Invalid project ID format")
            
        db = await get_database()
        result = await db.projects.delete_one({"_id": ObjectId(project_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
            
        return {"message": "Project deleted successfully"}
        
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid project ID format")
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
    
async def edit_deployment_url(project_id: str, deployment_url: str):
    try:
        db = await get_database()
        result = await db.projects.update_one({"_id": ObjectId(project_id)}, {"$set": {"deployment_url": deployment_url}})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Failed to change url (project not found or url already updated)")
        
        return {"message": "Deployment URL updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))