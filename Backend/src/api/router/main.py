from fastapi import APIRouter
from src.api.routes import todos, agent

api_router = APIRouter()
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])