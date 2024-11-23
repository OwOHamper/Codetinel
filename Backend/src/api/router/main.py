from fastapi import APIRouter
from src.api.routes import project

api_router = APIRouter()

api_router.include_router(project.router, prefix="/project", tags=["project"])
