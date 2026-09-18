"""Controller 层：登录、首页与关闭服务。"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.status import HTTP_302_FOUND

from app.config.config import AUTH_COOKIE, AUTH_TTL_SECONDS
from app.config.runtime import request_shutdown
from app.services.auth_service import auth_service
from app.views.auth_page_view import render_home_page, render_login_page
from app.views.auth_view import LoginInfo, LoginRequest, LoginResponse, SimpleResponse

router = APIRouter(tags=["auth"])


def _json(payload: LoginResponse | SimpleResponse) -> JSONResponse:
    """统一响应格式，HTTP 状态码恒为 200，业务码放在 body.code。"""
    return JSONResponse(status_code=200, content=payload.model_dump())


@router.get("/login", response_class=HTMLResponse, summary="登录页", include_in_schema=False)
def login_page(request: Request) -> Response:
    """已登录时直接跳到首页。"""
    if auth_service.verify_token(request.cookies.get(AUTH_COOKIE)) is not None:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)
    return render_login_page(request)


@router.post("/api/login", response_model=LoginResponse, summary="登录")
def login(payload: LoginRequest) -> JSONResponse:
    """校验写死的账号密码，成功后写入签名 Cookie。"""
    if not auth_service.verify_credentials(payload.username, payload.password):
        return _json(LoginResponse(code=401, body=[], msg="账号或密码错误"))

    token = auth_service.issue_token(payload.username)
    response = _json(
        LoginResponse(code=200, body=[LoginInfo(username=payload.username, redirect="/")], msg="success")
    )
    response.set_cookie(
        AUTH_COOKIE,
        token,
        max_age=AUTH_TTL_SECONDS,
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/logout", summary="退出登录", include_in_schema=False)
def logout() -> RedirectResponse:
    response = RedirectResponse("/login", status_code=HTTP_302_FOUND)
    response.delete_cookie(AUTH_COOKIE)
    return response


@router.get("/", response_class=HTMLResponse, summary="首页（需登录）", include_in_schema=False)
def home(request: Request) -> HTMLResponse:
    """首页门户：接口路径清单、数据管理入口、关闭服务。"""
    username = auth_service.verify_token(request.cookies.get(AUTH_COOKIE)) or ""
    return render_home_page(request, username)


@router.post("/api/shutdown", response_model=SimpleResponse, summary="关闭服务（需登录）")
def shutdown(request: Request) -> JSONResponse:
    """优雅关闭服务；开发模式（热重载）下无法关闭，提示用 Ctrl+C。"""
    if auth_service.verify_token(request.cookies.get(AUTH_COOKIE)) is None:
        return _json(SimpleResponse.fail(401, "请先登录"))
    if not request_shutdown():
        return _json(SimpleResponse.fail(400, "当前为开发模式（热重载），请在终端按 Ctrl+C 关闭"))
    return _json(SimpleResponse.ok())
