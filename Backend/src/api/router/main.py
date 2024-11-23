from fastapi import APIRouter
<<<<<<< HEAD
from src.api.routes import todos, agent

api_router = APIRouter()
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
=======
from src.api.routes import todos, project

api_router = APIRouter()

api_router.include_router(project.router, prefix="/project", tags=["project"])
>>>>>>> 121a7a1a0bfd8120280edc304ea03afc0e702456
