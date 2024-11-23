from fastapi import FastAPI, BackgroundTasks
from typing import Dict, Optional
import os
from dotenv import load_dotenv
from uuid import uuid4
from src.db.mongodb import get_database
from datetime import datetime
from src.AI.agents.pentest_agent import PentestAgent

load_dotenv()

app = FastAPI()

# Initialize the pentest agent
agent = PentestAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    target_url=os.getenv("TARGET_URL", "http://example.com")
)

async def store_task_status(task_id: str, status: Dict):
    """Store task status in MongoDB"""
    db = await get_database()
    await db.agent_tasks.update_one(
        {"task_id": task_id},
        {"$set": {
            **status,
            "updated_at": datetime.utcnow()
        }},
        upsert=True
    )

async def process_agent_task(task_id: str, message: str, context: Optional[Dict] = None):
    """Process agent task and store results in MongoDB"""
    try:
        # Update initial status
        await store_task_status(task_id, {
            "task_id": task_id,
            "status": "processing",
            "message": message,
            "created_at": datetime.utcnow()
        })

        # Process message
        response = await agent.process_message(message, context)
        
        # Store success result
        await store_task_status(task_id, {
            "status": "completed",
            "result": response
        })

    except Exception as e:
        # Store error result
        await store_task_status(task_id, {
            "status": "failed",
            "error": str(e)
        })

@app.post("/agent/process")
async def process_message(
    message: str,
    background_tasks: BackgroundTasks,
    context: Optional[Dict] = None
) -> Dict:
    """Start a new agent task in the background"""
    task_id = str(uuid4())
    
    # Add task to background tasks
    background_tasks.add_task(
        process_agent_task,
        task_id=task_id,
        message=message,
        context=context
    )
    
    return {
        "task_id": task_id,
        "status": "processing"
    }

@app.get("/agent/status/{task_id}")
async def get_task_status(task_id: str) -> Dict:
    """Get the status of an agent task"""
    db = await get_database()
    task = await db.agent_tasks.find_one({"task_id": task_id})
    if task:
        task["_id"] = str(task["_id"])
        return task
    return {"status": "not_found"}

@app.post("/agent/scan-endpoint")
async def scan_endpoint(
    endpoint: str,
    background_tasks: BackgroundTasks,
    context: Optional[Dict] = None
) -> Dict:
    """Start a security scan of an endpoint"""
    task_id = str(uuid4())
    
    background_tasks.add_task(
        process_agent_task,
        task_id=task_id,
        message=f"Perform a security assessment of the endpoint: {endpoint}",
        context={"endpoint": endpoint, **(context or {})}
    )
    
    return {
        "task_id": task_id,
        "status": "processing"
    }