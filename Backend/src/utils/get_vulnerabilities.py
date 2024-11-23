from bson import ObjectId
from src.db.mongodb import get_database
from fastapi import HTTPException
import traceback

async def get_vulnerabilities_by_id(project_id: str):
    try:
        # Convert string ID to MongoDB ObjectId
        project_obj_id = ObjectId(project_id)
        
        # Get database instance
        db = await get_database()
        # Find project and get vulnerabilities
        project = await db.projects.find_one({"_id": project_obj_id})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        return  project.get("vulnerabilities", [])
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_vulnerability_by_id(project_id: str, vulnerability_id: str):
    try:
        project_obj_id = ObjectId(project_id)
        db = await get_database()
        project = await db.projects.find_one({"_id": project_obj_id})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        # Find the specific vulnerability
        vulnerability = project.get("vulnerabilities", []).get(vulnerability_id)
        
        if not vulnerability:
            raise HTTPException(status_code=404, detail="Vulnerability not found")
            
        return vulnerability # Return single vulnerability instead of list
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
