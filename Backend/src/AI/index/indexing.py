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
import fnmatch

# Define base directory for repositories
BASE_REPOS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data")
# Map of repository URLs to their local paths
REPO_PATHS = {
    "https://github.com/juice-shop/juice-shop": os.path.join(BASE_REPOS_DIR, "juice-shop"),
    "https://github.com/DiogoMRSilva/websitesVulnerableToSSTI": os.path.join(BASE_REPOS_DIR, "websitesVulnerableToSSTI")
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
    '.vscode',
    'test',  # Skip test directories
    'frontend/src/assets',  # Skip asset files
    'frontend',
    'rsn',  # Skip rsn directory
    'views'  # Skip views directory
}

# Files to ignore (relative paths)
IGNORED_FILES = {
    'karma.conf.js',
    'webpack.angular.js',
    '.eslintrc.js',
    '.stylelintrc.js',
    'polyfills.ts',
    'test.ts',
    'index.html',
    'environment.ts',
    'environment.prod.ts',
    '*.spec.ts',  # Skip all test spec files
    '*.min.js',   # Skip minified files
    'three.js'    # Skip three.js library
}

def should_ignore_path(path: str) -> bool:
    """Check if a path should be ignored"""
    path_parts = Path(path).parts
    
    # Check ignored directories
    if any(ignored_dir in path_parts for ignored_dir in IGNORED_DIRS):
        return True
        
    # Check ignored files
    file_name = os.path.basename(path)
    if any(fnmatch.fnmatch(file_name, pattern) for pattern in IGNORED_FILES):
        return True
        
    return False

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
                    
                    # print(f"Read file {relative_path}")
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
            chunk_size=1500,
            chunk_overlap=300,
            separators=["\n\n", "\n", " ", ""]
        )
        splits = text_splitter.split_documents(documents)
        print(f"Split into {len(splits)} chunks")
        
        # Add project metadata to each chunk
        for split in splits:
            split.metadata["project_id"] = project_id
        
        # Get the ChromaDB client and its max batch size
        # chroma_client = Chroma(persist_directory="./chroma_db")
        max_batch_size = 166 
        
        # Create embeddings
        print("Creating embeddings and storing in ChromaDB")
        embeddings = OpenAIEmbeddings()
        
        # Process splits in batches
        for i in range(0, len(splits), max_batch_size):
            batch = splits[i:i + max_batch_size]
            vectorstore = Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                collection_name=f"project_{project_id}",
                persist_directory="./chroma_db"
            )
            # vectorstore.persist()
            print(f"Processed batch {i//max_batch_size + 1} of {(len(splits)-1)//max_batch_size + 1}")
        
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
