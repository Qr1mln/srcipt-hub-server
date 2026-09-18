"""应用入口：uvicorn main:app --reload"""
import uvicorn
from fastapi import FastAPI

from app.controllers import api_router
from app.config.config import settings


def create_app() -> FastAPI:
    """应用工厂，便于测试与多环境初始化。"""
    application = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description=settings.description,
    )
    application.include_router(api_router)
    return application

if __name__ == "__main__":
    # 工厂模式必须显式声明 factory=True，否则 uvicorn 会把 create_app 当作 ASGI 应用调用
    uvicorn.run("main:create_app", factory=True, host="127.0.0.1", port=8000, reload=True)
