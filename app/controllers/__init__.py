from fastapi import APIRouter

from app.controllers.auth_controller import router as auth_router
from app.controllers.category_controller import router as category_router
from app.controllers.zjm_controller import router as zjm_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(zjm_router)
api_router.include_router(category_router)

__all__ = ["api_router"]
