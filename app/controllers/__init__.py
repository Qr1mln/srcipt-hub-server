from fastapi import APIRouter

from app.controllers.zjm_controller import router as zjm_router

api_router = APIRouter()
api_router.include_router(zjm_router)

__all__ = ["api_router"]
