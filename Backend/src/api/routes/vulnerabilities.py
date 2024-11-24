from fastapi import APIRouter, HTTPException
from bson import ObjectId
from src.db.mongodb import get_database
from src.api.utils.vulnerabilities import get_vulnerabilities_by_id, get_vulnerability_by_id
from fastapi import APIRouter

router = APIRouter()

@router.get("/get-vulnerabilities/{project_id}")
async def get_vulnerabilities_by_project(project_id: str):
    return await get_vulnerabilities_by_id(project_id) 

@router.get("/get-vulnerability/{project_id}/{vulnerability_id}")
async def get_vulnerability_by_project_vulnerability(project_id: str, vulnerability_id: str):
    return await get_vulnerability_by_id(project_id, vulnerability_id)
