import traceback
from fastapi import HTTPException, UploadFile, File, Form, BackgroundTasks
from src.db.mongodb import get_database
from src.utils.normalizer import normalize_csv
import pandas as pd
import json
from datetime import timezone, datetime
from bson import ObjectId
from src.AI.index.indexing import index_repository

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
