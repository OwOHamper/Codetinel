from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Optional
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from uuid import uuid4
from src.db.mongodb import get_database
from datetime import datetime, timezone

from src.AI.tools.custom_tool import CustomSearchTool
from src.AI.agents.base_agent import AgentManager
from src.config import settings

load_dotenv()

router = APIRouter()

# Initialize the agent manager
agent_manager = AgentManager(openai_api_key=settings.OPENAI_API_KEY)

async def store_task_status(task_id: str, status: Dict):
    """Store task status in MongoDB"""
    db = await get_database()
    await db.agent_tasks.update_one(
        {"task_id": task_id},
        {"$set": {
            **status,
            "updated_at": timezone.utc
        }},
        upsert=True
    )

async def get_stored_task_status(task_id: str) -> Dict:
    """Retrieve task status from MongoDB"""
    db = await get_database()
    task = await db.agent_tasks.find_one({"task_id": task_id})
    if task:
        task["_id"] = str(task["_id"])
        return task
    return {"status": "not_found"}

async def process_agent_task(task_id: str, message: str, thread_id: str):
    """Process agent task and store results in MongoDB"""
    try:
        # Update initial status
        await store_task_status(task_id, {
            "task_id": task_id,
            "thread_id": thread_id,
            "status": "processing",
            "message": message,
            "created_at": timezone.utc
        })

        # Process message
        response = await agent_manager.process_message(message, thread_id)
        
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

@router.post("/process")
async def process_message(
    message: str,
    background_tasks: BackgroundTasks,
    thread_id: Optional[str] = None
) -> Dict:
    """
    Start a new agent task in the background
    """
    # Generate IDs
    task_id = str(uuid4())
    thread_id = thread_id or str(uuid4())
    
    # Add task to background tasks
    background_tasks.add_task(
        process_agent_task,
        task_id=task_id,
        message=message,
        thread_id=thread_id
    )
    
    return {
        "task_id": task_id,
        "thread_id": thread_id,
        "status": "processing"
    }

@router.get("/status/{task_id}")
async def get_task_status(task_id: str) -> Dict:
    """
    Get the status of an agent task
    """
    task = await get_stored_task_status(task_id)
    if task["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/thread/{thread_id}")
async def get_thread_history(thread_id: str) -> Dict:
    """
    Get all tasks and responses for a specific thread
    """
    db = await get_database()
    cursor = db.agent_tasks.find(
        {"thread_id": thread_id},
        sort=[("created_at", 1)]
    )
    
    history = []
    async for task in cursor:
        task["_id"] = str(task["_id"])
        history.append(task)
    
    if not history:
        raise HTTPException(status_code=404, detail="Thread not found")
        
    return {
        "thread_id": thread_id,
        "history": history
    }