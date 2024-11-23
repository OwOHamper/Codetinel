import os
import shutil
from typing import Dict, Any
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from src.db.mongodb import get_database
from bson import ObjectId
from langchain_core.documents import Document
import traceback

# Define base directory for repositories
BASE_REPOS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data")
# Map of repository URLs to their local paths
REPO_PATHS = {
    "https://github.com/juice-shop/juice-shop": os.path.join(BASE_REPOS_DIR, "juice-shop")
    # Add more repositories as needed
}

# Define which file extensions to include
CODE_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', 
    '.hpp', '.h', '.cs', '.go', '.rs', '.php', '.rb', '.swift',
    '.kt', '.kts', '.scala', '.sc', '.sql', '.html', '.css',
    '.scss', '.sass', '.less', '.vue', '.svelte'
}

# Directories to ignore
IGNORED_DIRS = {
    'node_modules',
    'venv',
    '.git',
    '__pycache__',
    'dist',
    'build',
    'coverage',
    '.next',
    '.idea',
    '.vscode'
}

def should_ignore_path(path: str) -> bool:
    """Check if a path should be ignored"""
    path_parts = Path(path).parts
    return any(ignored_dir in path_parts for ignored_dir in IGNORED_DIRS)

def get_local_repo_path(repo_url: str) -> str:
    """Get the local path for a repository URL"""
    if repo_url not in REPO_PATHS:
        raise Exception(f"Repository {repo_url} is not configured in REPO_PATHS")
    
    local_path = REPO_PATHS[repo_url]
    if not os.path.exists(local_path):
        raise Exception(f"Repository path {local_path} does not exist")
        
    return local_path

def is_code_file(file_path: str) -> bool:
    """Check if a file is a code file based on its extension"""
    return Path(file_path).suffix.lower() in CODE_EXTENSIONS

def read_code_files(repo_path: str) -> list[Document]:
    """Recursively read all code files from the repository"""
    documents = []
    
    for root, _, files in os.walk(repo_path):
        # Skip ignored directories
        if should_ignore_path(root):
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            if is_code_file(file_path):
                try:
                    # Get relative path for metadata
                    relative_path = os.path.relpath(file_path, repo_path)
                    
                    # Skip if the file is in an ignored directory
                    if should_ignore_path(relative_path):
                        continue
                    
                    # Read the file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Create a Document with metadata
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": relative_path,
                            "file_type": Path(file_path).suffix.lower(),
                            "file_name": os.path.basename(file_path)
                        }
                    )
                    documents.append(doc)
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")
                    continue
    
    return documents

async def index_repository(project_id: str, repo_url: str) -> Dict[str, Any]:
    """
    Index a locally installed repository using LangChain and ChromaDB
    """
    try:
        # Get the local repository path
        repo_path = get_local_repo_path(repo_url)
        print(f"Using local repository at {repo_path}")
        
        # Read all code files
        documents = read_code_files(repo_path)
        print(f"Loaded {len(documents)} code files")
        
        if not documents:
            raise Exception("No code files found in repository")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        splits = text_splitter.split_documents(documents)
        print(f"Split into {len(splits)} chunks")
        
        # Add project metadata to each chunk
        for split in splits:
            split.metadata["project_id"] = project_id
        
        # Create embeddings and store in ChromaDB
        print("Creating embeddings and storing in ChromaDB")
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            collection_name=f"project_{project_id}",
            persist_directory="./chroma_db"
        )
        
        # Persist the vectorstore
        vectorstore.persist()
        
        # Update indexing status
        db = await get_database()
        await db.projects.update_one(
            {"_id": ObjectId(project_id)}, 
            {"$set": {
                "indexing_status": "completed",
                "indexed_files_count": len(documents),
                "chunks_count": len(splits)
            }}
        )
        
        return {
            "status": "success",
            "message": f"Indexed {len(splits)} chunks from {len(documents)} code files",
            "document_count": len(documents),
            "chunks_count": len(splits)
        }
        
    except Exception as e:
        print(traceback.format_exc())
        # Update status to failed
        try:
            db = await get_database()
            await db.projects.update_one(
                {"_id": ObjectId(project_id)}, 
                {"$set": {
                    "indexing_status": "failed",
                    "error_message": str(e)
                }}
            )
        except:
            pass
            
        return {
            "status": "error",
            "message": str(e)
        }
