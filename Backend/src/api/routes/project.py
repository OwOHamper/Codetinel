from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from src.AI.index.indexing import index_repository
from src.db.mongodb import get_database
from datetime import datetime
from bson import ObjectId
import pandas as pd
import json
from src.api.utils.normalizer import normalize_csv
from src.api.utils.project import create_project, delete_project, edit_deployment_url   
import traceback
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

router = APIRouter()

@router.post("/create")
async def create_project_route(
    background_tasks: BackgroundTasks,
    project_name: str = Form(...),
    csv_file: UploadFile = File(...),
    url: str = Form(...),
    deployment_url: str = Form(...)
):
    return await create_project(project_name, csv_file, url, deployment_url, background_tasks)

@router.delete("/delete")
async def delete_project_route(project_id: str = Form(...)):
    return await delete_project(project_id)

@router.post("/edit-deployment-url")
async def edit_deployment_url_route(project_id: str = Form(...), deployment_url: str = Form(...)):
    return await edit_deployment_url(project_id, deployment_url)

@router.get("/indexing-status/{project_id}")
async def get_indexing_status(project_id: str):
    """Get the current indexing status for a project"""
    try:
        db = await get_database()
        project = await db.projects.find_one({"_id": ObjectId(project_id)})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return {
            "status": project.get("indexing_status", "unknown"),
            "project_name": project["project_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

embeddings = OpenAIEmbeddings()

@router.get("/search/{project_id}")
async def search_codebase(project_id: str, query: str):
    """Test the vector search functionality"""
    try:
        

        # Load the existing collection
        vectorstore = Chroma(
            collection_name=f"project_{project_id}",
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        
        # Perform similarity search
        results = vectorstore.similarity_search(query, k=10)
        
        return {
            "results": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": doc.metadata.get("score", None)  # If available
                }
                for doc in results
            ]
        }
        
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/collection-info/{project_id}")
async def get_collection_info(project_id: str):
    """Get information about the ChromaDB collection for a project"""
    try:
        from langchain_community.vectorstores import Chroma
        
        # Load the existing collection
        vectorstore = Chroma(
            collection_name=f"project_{project_id}",
            persist_directory="./chroma_db"
        )
        
        # Get collection stats
        collection = vectorstore._collection
        return {
            "collection_name": collection.name,
            "count": collection.count(),
            "metadata": collection.metadata
        }
        
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/retry-indexing/{project_id}")
async def retry_indexing(project_id: str, background_tasks: BackgroundTasks):
    """Retry indexing for a failed project"""
    try:
        db = await get_database()
        project = await db.projects.find_one({"_id": ObjectId(project_id)})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        if project.get("indexing_status") != "failed":
            raise HTTPException(
                status_code=400, 
                detail="Can only retry indexing for failed projects"
            )
            
        # Reset indexing status to pending
        await db.projects.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": {"indexing_status": "pending"}}
        )
        
        # Add background task for indexing
        background_tasks.add_task(
            index_repository,
            project_id=project_id,
            repo_url=project["url"]
        )
        
        return {
            "message": "Indexing retry started",
            "project_id": project_id
        }
        
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_all_projects")
async def get_all_projects():
    """Get all projects from the database"""
    try:
        db = await get_database()
        projects = await db.projects.find().to_list(length=None)
        for project in projects:
            project["_id"] = str(project["_id"])
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")