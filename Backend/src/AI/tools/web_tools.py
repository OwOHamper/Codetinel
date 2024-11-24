from langchain.tools import BaseTool, tool
from pydantic import BaseModel, Field
import aiohttp
from typing import Optional, Dict, Any
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import traceback

def create_web_request(base_url: str):
    """Creates a web request tool with pre-configured base URL"""
    
    @tool
    async def web_request(
        method: str = Field(..., description="HTTP method (GET, POST, etc.)"),
        path: str = Field(..., description="URL path to request"),
        headers: Optional[Dict[str, str]] = Field(default=None, description="Request headers"),
        data: Optional[Dict[str, Any]] = Field(default=None, description="Request body data")
    ) -> Dict[str, Any]:
        """Make HTTP requests to the target web application"""
        # Get the actual values from the Field objects
        method = method if isinstance(method, str) else method.default
        path = path if isinstance(path, str) else path.default
        headers = headers.default if hasattr(headers, 'default') else headers
        data = data.default if hasattr(data, 'default') else data

        # Validate and normalize method
        method = method.upper()
        if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
            return {
                "error": f"Invalid HTTP method: {method}",
                "status": 400,
                "data": None
            }

        # Handle case where path is a full URL
        if path.lower().startswith(('http://', 'https://')):
            if not path.lower().startswith(base_url.lower()):
                return {
                    "error": f"Path must be relative or start with base URL: {base_url}",
                    "status": 400,
                    "data": None
                }
            # Extract the path portion from the full URL
            path = path[len(base_url.rstrip('/')):]

        # Clean up path
        path = path.lstrip('/')
        
        print("Using web request tool")
        print(f"Method: {method}")
        print(f"Path: {path}")
        print(f"Headers: {headers}")
        print(f"Data: {data}")
        print(f"Base URL: {base_url}")
        
        url = f"{base_url.rstrip('/')}/{path}"
        
        try:
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
                        # Limit response data size (e.g., to 100KB)
                        if isinstance(response_data, str) and len(response_data) > 80000:
                            response_data = response_data[:80000] + "... (truncated)"
                        elif isinstance(response_data, dict):
                            response_data_str = str(response_data)
                            if len(response_data_str) > 80000:
                                response_data = {"warning": "Response was truncated due to size", "truncated_data": str(response_data)[:100000] + "..."}
                    except:
                        response_data = await response.text()
                        if len(response_data) > 80000:
                            response_data = response_data[:80000] + "... (truncated)"
                    
                    return {
                        "status": status,
                        "headers": response_headers,
                        "data": response_data
                    }
        except aiohttp.ClientError as e:
            return {
                "error": f"Request failed: {str(e)}",
                "status": 500,
                "data": None
            }
    
    return web_request

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