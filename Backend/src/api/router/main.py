from fastapi import APIRouter
from src.api.routes import project
from src.api.routes import agent

api_router = APIRouter()

api_router.include_router(project.router, prefix="/project", tags=["project"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])