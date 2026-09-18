from fastapi import APIRouter

from app.controllers.greeting_controller import router as greeting_router

api_router = APIRouter()
api_router.include_router(greeting_router)

__all__ = ["api_router"]
