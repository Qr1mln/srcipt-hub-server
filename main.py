"""应用入口。

用法：
    python main.py                    # 源码运行，默认 127.0.0.1:8000，带热重载
    python main.py --port 8100        # 指定端口
    python main.py --host 0.0.0.0     # 指定监听地址
    dist\\zjm_server.exe --port 8100   # 打包后运行
    zjm_server.exe --help             # 查看参数

直接用 uvicorn 启动时，host/port 交给 uvicorn 自己解析：
    uvicorn main:create_app --factory --reload --host 0.0.0.0 --port 8100
"""

import argparse

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.config import DEFAULT_CORS_ORIGINS, DEFAULT_HOST, DEFAULT_PORT, is_frozen, settings
from app.config.logger import LOG_FILE, setup_logging
from app.controllers import api_router
from app.middlewares import RequestLoggingMiddleware
from app.repositories.zjm_repository import init_db

# 参数校验失败时的中文说明
VALIDATION_MESSAGES = {
    "missing": "不能为空",
    "string_too_short": "长度不足",
    "string_too_long": "长度超出限制",
    "string_type": "必须是字符串",
    "json_invalid": "JSON 格式错误",
}


def create_app() -> FastAPI:
    """应用工厂：注册中间件、初始化数据库、注册路由与统一异常响应。"""
    application = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description=settings.description,
    )

    setup_logging()

    # 请求日志（后添加的中间件在外层）：先加日志、再加 CORS，
    # 这样 CORS 预检 OPTIONS 由外层直接响应，不写进日志，避免噪声
    application.add_middleware(RequestLoggingMiddleware)

    # 跨域：默认放开所有来源、方法与请求头（含 OPTIONS 预检），来源列表见 config.DEFAULT_CORS_ORIGINS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=DEFAULT_CORS_ORIGINS,
        allow_credentials=False,  # 本服务不使用 Cookie；该项为 True 时 allow_origins 不能是 "*"
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_db()
    application.include_router(api_router)

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
        """参数校验失败时也返回统一响应格式。"""
        errors = exc.errors()
        if errors:
            first = errors[0]
            field = ".".join(str(part) for part in first.get("loc", ()) if part != "body")
            reason = VALIDATION_MESSAGES.get(first.get("type", ""), "参数不合法")
            message = f"参数校验失败：{field} {reason}"
        else:
            message = "参数校验失败"
        return JSONResponse(status_code=200, content={"code": 400, "body": [], "msg": message})

    return application


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数：--host / --port。"""
    parser = argparse.ArgumentParser(prog="zjm_server", description=settings.description)
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"监听地址，默认 {DEFAULT_HOST}")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"监听端口，默认 {DEFAULT_PORT}")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    app = create_app()
    if is_frozen():
        # 打包后无法用 "main:create_app" 字符串导入，也不能用 reload，直接传 app 对象
        print(f"ZJM Server 已启动：http://{args.host}:{args.port}  (Ctrl+C 退出)")
        print(f"日志文件：{LOG_FILE}")
        uvicorn.run(app, host=args.host, port=args.port, access_log=False)
    else:
        # 工厂模式必须显式声明 factory=True，否则 uvicorn 会把 create_app 当作 ASGI 应用调用
        uvicorn.run("main:create_app", factory=True, host=args.host, port=args.port, reload=True, access_log=False)
