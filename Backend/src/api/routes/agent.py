from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel
from src.AI.agents.pentest_agent import PentestAgent
from src.config import settings
from datetime import datetime, timezone
from uuid import uuid4
from src.db.mongodb import get_database
import traceback

router = APIRouter()

class VulnerabilityTestRequest(BaseModel):
    project_id: str
    vulnerability_type: str
    endpoint: str
    additional_context: str = None
    file_context: str = None

async def store_task_status(task_id: str, status: Dict):
    """Store task status in MongoDB"""
    db = await get_database()
    await db.agent_tasks.update_one(
        {"task_id": task_id},
        {"$set": {
            **status,
            "updated_at": datetime.now(tz=timezone.utc)
        }},
        upsert=True
    )

async def process_pentest_task(
    task_id: str,
    project_id: str,
    vulnerability_type: str,
    endpoint: str,
    additional_context: str = None,
    file_context: str = None
):
    """Process pentest task and store results"""
    try:
        # Initialize pentest agent with the provided project_id
        pentest_agent = PentestAgent(
            openai_api_key=settings.OPENAI_API_KEY,
            project_id=project_id,
            target_url="http://localhost:3000",  # Configure this in settings
            model_name="gpt-4",
            temperature=0
        )
        
        # Update initial status
        await store_task_status(task_id, {
            "task_id": task_id,
            "status": "processing",
            "project_id": project_id,
            "vulnerability_type": vulnerability_type,
            "endpoint": endpoint,
            "created_at": datetime.now(tz=timezone.utc)
        })

        # Process vulnerability test
        response = await pentest_agent.test_vulnerability(
            vulnerability_type=vulnerability_type,
            endpoint=endpoint,
            additional_context=additional_context,
            file_context=file_context
        )
        
        # Store success result
        await store_task_status(task_id, {
            "status": "completed",
            "result": response
        })

    except Exception as e:
        print(f"Error in pentest task: {str(e)}")
        print(traceback.format_exc())
        # Store error result
        await store_task_status(task_id, {
            "status": "failed",
            "error": str(e)
        })

@router.post("/pentest/test")
async def test_vulnerability(
    request: VulnerabilityTestRequest,
    background_tasks: BackgroundTasks,
) -> Dict:
    """
    Start a new pentest task
    """
    task_id = str(uuid4())
    
    # Add task to background tasks
    background_tasks.add_task(
        process_pentest_task,
        task_id=task_id,
        project_id=request.project_id,
        vulnerability_type=request.vulnerability_type,
        endpoint=request.endpoint,
        additional_context=request.additional_context,
        file_context=request.file_context
    )
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": f"Testing {request.vulnerability_type} vulnerability on {request.endpoint}"
    }

@router.get("/pentest/status/{task_id}")
async def get_pentest_status(task_id: str) -> Dict:
    """Get the status of a pentest task"""
    db = await get_database()
    task = await db.agent_tasks.find_one({"task_id": task_id})
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    task["_id"] = str(task["_id"])
    return task