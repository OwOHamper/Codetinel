from typing import Dict, Any, List, Optional
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from langchain.agents import create_tool_calling_agent, AgentExecutor

class BaseAgentManager:
    """Base class for all agent implementations"""
    
    def __init__(
        self,
        openai_api_key: str,
        model_name: str = "gpt-4o",
        temperature: float = 0,
        system_message: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None
    ):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            api_key=openai_api_key
        )
        
        # Initialize tools
        self.tools = tools or []
        
        self.system_message = system_message
    
        # Create the agent with system message
        self.agent = create_tool_calling_agent(
            self.llm, 
            self.tools, 
            system_message
        )
        
        # Create the executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )

    async def process_message(
        self,
        message: str,
        # context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a message using the agent"""
        # Run the agent
        response = await self.agent_executor.invoke(
            {
                "input": message, 
                # **(context or {})
            }
        )
        
        return response