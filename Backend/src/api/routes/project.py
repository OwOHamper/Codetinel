from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from src.db.mongodb import get_database
from src.models.todo import Todo, TodoCreate
from datetime import datetime
from bson import ObjectId
import pandas as pd
import json
from src.utils.normalizer import DataNormalizer
from src.api.utils.project import get_vulnerabilities, create_project
import traceback
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

router = APIRouter()

@router.post("/create")
async def create_project_route(
    background_tasks: BackgroundTasks,
    project_name: str = Form(...),
    csv_file: UploadFile = File(...),
    url: str = Form(...)
):
    return await create_project(project_name, csv_file, url, background_tasks)

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

