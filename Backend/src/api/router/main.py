from fastapi import APIRouter
from src.api.routes import project
from src.api.routes import agent
from src.api.routes import vulnerabilities

api_router = APIRouter()

api_router.include_router(project.router, prefix="/project", tags=["project"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
api_router.include_router(vulnerabilities.router, prefix="/vulnerabilities", tags=["vulnerabilities"])