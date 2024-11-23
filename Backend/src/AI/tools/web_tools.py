from langchain.tools import BaseTool, tool
from pydantic import BaseModel, Field
import aiohttp
from typing import Optional, Dict, Any
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import traceback

@tool
async def web_request(
    method: str = Field(..., description="HTTP method (GET, POST, etc.)"),
    path: str = Field(..., description="URL path to request"),
    headers: Optional[Dict[str, str]] = Field(default=None, description="Request headers"),
    data: Optional[Dict[str, Any]] = Field(default=None, description="Request body data"),
    base_url: str = Field(..., description="Base URL for the request")
) -> Dict[str, Any]:
    """Make HTTP requests to the target web application"""
    # Get the actual values from the Field objects
    headers = {} if headers is None else headers
    data = {} if data is None else data
    
    print("Using web request tool")
    print(f"Method: {method}")
    print(f"Path: {path}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    print(f"Base URL: {base_url}")
    
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=method,
            url=url,
            headers=headers,
            json=data
        ) as response:
            status = response.status
            response_headers = dict(response.headers)
            try:
                response_data = await response.json()
            except:
                response_data = await response.text()
            
            return {
                "status": status,
                "headers": response_headers,
                "data": response_data
            }

def create_code_search(project_id: str, persist_directory: str = "./chroma_db"):
    """Creates a code search tool with pre-configured project ID"""
    
    @tool
    async def code_search(
        query: str = Field(..., description="Search query to find relevant code")
    ) -> Dict[str, Any]:
        """
        Search through the project's codebase to find relevant code snippets.
        Use this when you need to:
        - Find specific implementations
        - Look up how certain features are coded
        - Find security-relevant code sections
        - Understand the codebase structure
        """
        print("Using code search tool")
        try:
            embeddings = OpenAIEmbeddings()
            vectorstore = Chroma(
                collection_name=f"project_{project_id}",
                persist_directory=persist_directory,
                embedding_function=embeddings
            )
            
            # Ensure k is a concrete integer
            
            # Perform similarity search with concrete integer
            results = vectorstore.similarity_search(query, k=10)
            
            # Format results
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "file_path": doc.metadata.get("source", "Unknown"),
                    "file_type": doc.metadata.get("file_type", "Unknown"),
                    "file_name": doc.metadata.get("file_name", "Unknown")
                })
            
            return {
                "query": query,
                "results_count": len(formatted_results),
                "results": formatted_results
            }
            
        except Exception as e:
            print(traceback.format_exc())
            return {
                "error": str(e),
                "query": query,
                "results_count": 0,
                "results": []
            }
    
    return code_search