from fastapi import APIRouter

from app.api import items, tasks, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(items.router)
api_router.include_router(tasks.router)
