from langchain_community.document_loaders import GitLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import tempfile
import os
import shutil
from typing import Dict, Any

async def index_repository(project_id: str, repo_url: str) -> Dict[str, Any]:
    """
    Clone and index a git repository using LangChain and ChromaDB
    """
    # Create a temporary directory for the repo
    temp_dir = tempfile.mkdtemp()
    try:
        # Load git repository
        loader = GitLoader(
            clone_url=repo_url,
            repo_path=temp_dir,
            branch="master"
        )
        
        # Load all documents
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        splits = text_splitter.split_documents(documents)
        
        # Add metadata to track project association
        for split in splits:
            split.metadata["project_id"] = project_id
        
        # Create embeddings and store in ChromaDB
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            collection_name=f"project_{project_id}",
            persist_directory="./chroma_db"
        )
        
        # Persist the vectorstore
        vectorstore.persist()
        
        return {
            "status": "success",
            "message": f"Indexed {len(splits)} document chunks",
            "document_count": len(splits)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
