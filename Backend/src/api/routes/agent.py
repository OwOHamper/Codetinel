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
from src.api.utils.vulnerabilities import get_vulnerabilities_by_id

router = APIRouter()

class VulnerabilityTestRequest(BaseModel):
    project_id: str
    vulnerability_id: str

async def store_task_status(task_id: str, status: Dict):
    """Store task status in MongoDB and update vulnerability status"""
    db = await get_database()
    
    # First store/update the task status
    await db.agent_tasks.update_one(
        {"task_id": task_id},
        {"$set": {
            **status,
            "updated_at": datetime.now(tz=timezone.utc)
        }},
        upsert=True
    )
    
    # If we have project_id and vulnerability_id, update the vulnerability status
    if "project_id" in status and "vulnerability_id" in status:
        project_id = status["project_id"]
        vulnerability_id = status["vulnerability_id"]
        
        # Build the complete last_test object first
        last_test = {
            "task_id": task_id,
            "timestamp": datetime.now(tz=timezone.utc),
            "status": status["status"]
        }
        
        # Add optional fields to last_test
        if "result" in status:
            last_test["result"] = status["result"]
        if "error" in status:
            last_test["error"] = status["error"]
            
        # Create the update data
        vulnerability_update = {
            f"vulnerabilities.{vulnerability_id}.status": status["status"],
            f"vulnerabilities.{vulnerability_id}.last_test": last_test
        }
        
        # Update the project's vulnerability status
        await db.projects.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": vulnerability_update}
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
    vulnerability_id: str,
    vulnerability_type: str,
    additional_context: str = None,
    file_context: str = None,
    line_number: int = None
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
        
        # Update status to processing
        await store_task_status(task_id, {
            "status": "processing",
            "project_id": project_id,
            "vulnerability_id": vulnerability_id,
            "vulnerability_type": vulnerability_type,
            "started_at": datetime.now(tz=timezone.utc)
        })

        # Process vulnerability test
        response = await pentest_agent.test_vulnerability(
            vulnerability_type=vulnerability_type,
            additional_context=additional_context,
            endpoint=deployment_url,
            file_context=file_context,
            line_number=line_number
        )   
        
        # Store success result
        await store_task_status(task_id, {
            "status": "completed",
            "result": response,
            "project_id": project_id,
            "vulnerability_id": vulnerability_id,
            "completed_at": datetime.now(tz=timezone.utc)
        })

    except Exception as e:
        print(f"Error in pentest task: {str(e)}")
        print(traceback.format_exc())
        # Store error result
        await store_task_status(task_id, {
            "status": "failed",
            "error": str(e),
            "project_id": project_id,
            "vulnerability_id": vulnerability_id,
            "failed_at": datetime.now(tz=timezone.utc)
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
    # Convert file context to path:line format if it exists
    file_context = vulnerability.get("location")
    print("File context:", file_context)
    middle_line = None
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
        vulnerability_id=request.vulnerability_id,
        vulnerability_type=vulnerability["vulnerability"],
        additional_context=vulnerability.get("details"),
        file_context=file_context,
        line_number=middle_line or None,
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