from bson import ObjectId
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel
from src.AI.agents.pentest_agent import PentestAgent
from src.config import settings
from datetime import datetime, timezone
from uuid import uuid4
from src.db.mongodb import get_database
import traceback
import os
from pathlib import Path
from src.utils.get_vulnerabilities import get_vulnerabilities_by_id

router = APIRouter()

class VulnerabilityTestRequest(BaseModel):
    project_id: str
    vulnerability_id: str

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

async def get_file_context(file_path: str, line_number: int, context_lines: int = 10) -> str:
    """
    Get file context around specific line number with additional lines above and below.
    
    Args:
        file_path: Relative path to the file from /data/juice-shop
        line_number: Target line number
        context_lines: Number of lines to include above and below (default 10)
    
    Returns:
        String containing the file context with line numbers
    """
    try:
        # Convert relative path to absolute path
        base_path = Path("data/juice-shop")
        abs_path = base_path / file_path.lstrip('/')
        
        if not abs_path.exists():
            return f"File not found: {file_path}"
            
        # Read file lines
        with open(abs_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Calculate start and end lines with context
        start_line = max(0, line_number - context_lines - 1)  # -1 for 0-based indexing
        end_line = min(len(lines), line_number + context_lines)
        
        # Extract relevant lines with context
        context_lines = lines[start_line:end_line]
        
        # Format output with line numbers
        output = []
        for i, line in enumerate(context_lines, start=start_line + 1):
            output.append(f"{i}|{line.rstrip()}")
            
        return "\n".join(output)
        
    except Exception as e:
        return f"Error reading file: {str(e)}"

async def process_pentest_task(
    task_id: str,
    project_id: str,
    vulnerability_type: str,
    additional_context: str = None,
    file_context: str = None
):
    """Process pentest task and store results"""
    try:
        # Parse file context if provided in format "path:line"
        if file_context and ":" in file_context:
            file_path, line_num = file_context.split(":")
            line_num = int(line_num)
            file_context = await get_file_context(file_path, line_num)
            
        print("Got file context:", file_context)
        
        db = await get_database()
        project = await db.projects.find_one({"_id": ObjectId(project_id)})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        deployment_url = project.get("deployment_url")
        
        # Initialize pentest agent with the provided project_id
        pentest_agent = PentestAgent(
            openai_api_key=settings.OPENAI_API_KEY,
            project_id=project_id,
            target_url=deployment_url,
            model_name="gpt-4o",
            temperature=0
        )
        
        # Update initial status
        await store_task_status(task_id, {
            "task_id": task_id,
            "status": "processing",
            "project_id": project_id,
            "vulnerability_type": vulnerability_type,
            "created_at": datetime.now(tz=timezone.utc)
        })

        # Process vulnerability test with enhanced file context
        response = await pentest_agent.test_vulnerability(
            vulnerability_type=vulnerability_type,
            additional_context=additional_context,
            endpoint=deployment_url,
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
    # Get vulnerability details from project
    vulnerabilities = await get_vulnerabilities_by_id(request.project_id)
    if not vulnerabilities:
        raise HTTPException(status_code=404, detail="Project or vulnerabilities not found")
        
    # Find the specific vulnerability
    vulnerability = vulnerabilities.get(request.vulnerability_id)
            
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    task_id = str(uuid4())
    print("Vulnerability:", vulnerability)
    # Convert file context to path:line format if it exists
    file_context = vulnerability.get("location")
    print("File context:", file_context)
    if file_context and isinstance(file_context, str):
        # Parse the Ruby-style string format
        try:
            # Remove curly braces and split by commas
            content = file_context.strip('{}').split(',')
            file_context_dict = {}
            
            for item in content:
                key, value = item.split('=>')
                # Clean up the strings
                key = key.strip().strip('"')
                value = value.strip()
                # Convert numeric values
                if value.isdigit():
                    value = int(value)
                else:
                    value = value.strip('"')
                file_context_dict[key] = value

            file_path = file_context_dict.get('file')
            start_line = file_context_dict.get('start_line')
            
            if file_path and start_line:
                # If end_line exists, use middle line, otherwise use start_line
                if 'end_line' in file_context_dict:
                    end_line = file_context_dict['end_line']
                    middle_line = start_line + ((end_line - start_line) // 2)
                else:
                    middle_line = start_line
                    
                file_context = f"{file_path}:{middle_line}"
        except Exception as e:
            print(f"Error parsing file context: {str(e)}")
            file_context = None

    print("File context:", file_context)
    # Add task to background tasks with vulnerability details
    background_tasks.add_task(
        process_pentest_task,
        task_id=task_id,
        project_id=request.project_id,
        vulnerability_type=vulnerability["vulnerability"],
        additional_context=vulnerability.get("details"),
        file_context=file_context
    )
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": f"Testing {vulnerability['vulnerability']} vulnerability"
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