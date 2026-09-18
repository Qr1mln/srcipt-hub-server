"""中间件：页面登录校验。"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.status import HTTP_302_FOUND

from app.config.config import AUTH_COOKIE
from app.services.auth_service import auth_service

# 需要登录才能访问的页面（API 保持开放，便于跨域前端直接调用）
PROTECTED_PAGES = ("/", "/admin")


class AuthGuardMiddleware(BaseHTTPMiddleware):
    """未登录访问受保护页面时重定向到登录页。"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if (
            request.method == "GET"
            and request.url.path in PROTECTED_PAGES
            and auth_service.verify_token(request.cookies.get(AUTH_COOKIE)) is None
        ):
            return RedirectResponse("/login", status_code=HTTP_302_FOUND)
        return await call_next(request)
