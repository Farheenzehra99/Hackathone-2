from fastapi import APIRouter
from .endpoints import tasks, auth, chat

api_router = APIRouter()
api_router.include_router(auth.router, prefix="", tags=["auth"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(chat.router, prefix="", tags=["chat"])