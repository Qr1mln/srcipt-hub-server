"""View 层：登录页与首页（门户）渲染。"""

from fastapi import Request
from fastapi.responses import HTMLResponse

from app.config.templates import templates

# 不在 OpenAPI 规范里的页面/文档路由，手动补进首页清单
PAGE_ROUTES = (
    ("GET", "/login", "登录页"),
    ("GET", "/", "首页（需登录）"),
    ("GET", "/admin", "数据管理页（需登录）"),
    ("GET", "/logout", "退出登录"),
    ("GET", "/docs", "Swagger 交互文档"),
    ("GET", "/redoc", "ReDoc 文档"),
    ("GET", "/openapi.json", "OpenAPI 规范 JSON"),
)


def render_login_page(request: Request, error: str | None = None) -> HTMLResponse:
    """登录页视图。"""
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": error},
    )


def _endpoint_rows(request: Request) -> list[dict[str, str]]:
    """页面路由 + OpenAPI 规范里的接口，生成首页接口清单（新增接口自动出现）。"""
    rows = [{"method": method, "path": path, "summary": summary} for method, path, summary in PAGE_ROUTES]
    for path, operations in request.app.openapi().get("paths", {}).items():
        for method, operation in operations.items():
            rows.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "summary": operation.get("summary") or "",
                }
            )
    return rows


def render_home_page(request: Request, username: str) -> HTMLResponse:
    """首页（门户）：接口路径清单 + 数据管理入口 + 关闭服务。"""
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"username": username, "endpoints": _endpoint_rows(request)},
    )
