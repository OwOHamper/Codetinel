from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import aiohttp
from typing import Optional, Dict, Any
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

class WebRequestInput(BaseModel):
    """Input for web request tool"""
    method: str = Field(..., description="HTTP method (GET, POST, etc.)")
    path: str = Field(..., description="URL path to request")
    headers: Optional[Dict[str, str]] = Field(default=None, description="Request headers")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Request body data")

class WebRequestTool(BaseTool):
    """Tool for making web requests to the target application"""
    name = "web_request"
    description = "Make HTTP requests to the target web application"
    args_schema = WebRequestInput
    
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url.rstrip('/')

    async def _arun(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> str:
        url = f"{self.base_url}/{path.lstrip('/')}"
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

class SecurityScanInput(BaseModel):
    """Input for security scan tool"""
    scan_type: str = Field(..., description="Type of security scan to perform")
    target_path: Optional[str] = Field(default="/", description="Specific path to scan")

# class SecurityScanTool(BaseTool):
#     """Tool for performing security scans"""
#     name = "security_scan"
#     description = "Perform security scans on the target application"
#     args_schema = SecurityScanInput
    
#     def __init__(self, target_url: str):
#         super().__init__()
#         self.target_url = target_url

#     async def _arun(
#         self,
#         scan_type: str,
#         target_path: Optional[str] = "/"
#     ) -> str:
#         # Implement different types of security scans
#         scans = {
#             "headers": self._scan_headers,
#             "xss": self._scan_xss,
#             "sqli": self._scan_sqli,
#             "csrf": self._scan_csrf
#         }
        
#         scanner = scans.get(scan_type.lower())
#         if not scanner:
#             return f"Unsupported scan type: {scan_type}"
            
#         return await scanner(target_path)

#     async def _scan_headers(self, path: str) -> Dict[str, Any]:
#         """Scan security headers"""
#         async with aiohttp.ClientSession() as session:
#             async with session.get(f"{self.target_url}/{path.lstrip('/')}") as response:
#                 headers = dict(response.headers)
#                 security_headers = {
#                     "X-Frame-Options": headers.get("X-Frame-Options"),
#                     "X-XSS-Protection": headers.get("X-XSS-Protection"),
#                     "X-Content-Type-Options": headers.get("X-Content-Type-Options"),
#                     "Content-Security-Policy": headers.get("Content-Security-Policy"),
#                     "Strict-Transport-Security": headers.get("Strict-Transport-Security")
#                 }
#                 return {
#                     "found_headers": security_headers,
#                     "missing_headers": [k for k, v in security_headers.items() if not v]
#                 }

#     # Implement other scan methods
#     async def _scan_xss(self, path: str) -> Dict[str, Any]:
#         # Implement XSS scanning logic
#         pass

#     async def _scan_sqli(self, path: str) -> Dict[str, Any]:
#         # Implement SQL injection scanning logic
#         pass

#     async def _scan_csrf(self, path: str) -> Dict[str, Any]:
#         # Implement CSRF scanning logic
#         pass

class CodeSearchInput(BaseModel):
    """Input for code search tool"""
    query: str = Field(..., description="Search query to find relevant code")
    k: int = Field(default=5, description="Number of results to return")

class CodeSearchTool(BaseTool):
    """Tool for searching code in the project's codebase"""
    name = "code_search"
    description = """
    Search through the project's codebase to find relevant code snippets.
    Use this when you need to:
    - Find specific implementations
    - Look up how certain features are coded
    - Find security-relevant code sections
    - Understand the codebase structure
    """
    args_schema = CodeSearchInput
    
    def __init__(self, project_id: str, persist_directory: str = "./chroma_db"):
        super().__init__()
        self.project_id = project_id
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()

    async def _arun(
        self,
        query: str,
        k: int = 5
    ) -> Dict[str, Any]:
        try:
            # Load the existing collection
            vectorstore = Chroma(
                collection_name=f"project_{self.project_id}",
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            
            # Perform similarity search
            results = vectorstore.similarity_search(query, k=k)
            
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
            return {
                "error": str(e),
                "query": query,
                "results_count": 0,
                "results": []
            }

    def _run(self, query: str, k: int = 5) -> Dict[str, Any]:
        """Sync version of the tool"""
        raise NotImplementedError("This tool only supports async execution")