from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from src.db.mongodb import get_database
from src.models.todo import Todo, TodoCreate
from datetime import datetime
from bson import ObjectId
import pandas as pd
import json
from src.utils.normalizer import DataNormalizer
from src.api.utils.project import get_vulnerabilities, create_project

router = APIRouter()

@router.post("/create")
async def create_project_route(project_name: str = Form(...), csv_file: UploadFile = File(...), url: str = Form(...)):
    return await create_project(project_name, csv_file, url)

