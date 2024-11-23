from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Optional, Dict, Any, List

class VulnerabilityResearchInput(BaseModel):
    """Input for vulnerability research tool"""
    vulnerability_type: str = Field(..., description="Type of vulnerability to research")
    tech_stack: Optional[str] = Field(default=None, description="Technology stack details")
    additional_context: Optional[str] = Field(default=None, description="Additional context about the vulnerability")

class VulnerabilityResearchTool(BaseTool):
    """Tool for researching vulnerability details and exploitation methods"""
    name = "vulnerability_research"
    description = "Research vulnerability details, exploitation methods, and security testing approaches"
    args_schema = VulnerabilityResearchInput
    
    def __init__(self, tavily_api_key: str):
        super().__init__()
        self.search = TavilySearchResults(
            api_key=tavily_api_key,
            max_results=3,
            search_depth="advanced"
        )

    async def _arun(
        self,
        vulnerability_type: str,
        tech_stack: Optional[str] = None,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        # Construct search query
        query = f"how to test {vulnerability_type} vulnerability"
        if tech_stack:
            query += f" in {tech_stack}"
        if additional_context:
            query += f" {additional_context}"
        
        # Search for vulnerability information
        results = await self.search.ainvoke({"query": query})
        
        # Process and structure the results
        return {
            "vulnerability_type": vulnerability_type,
            "research_results": results,
            "testing_approaches": self._extract_testing_approaches(results)
        }
    
    def _extract_testing_approaches(self, results: List[Dict]) -> List[str]:
        """Extract testing approaches from search results"""
        # Implement logic to extract testing steps from results
        # This would be enhanced with better parsing logic
        approaches = []
        for result in results:
            if "snippet" in result:
                approaches.append(result["snippet"])
        return approaches 