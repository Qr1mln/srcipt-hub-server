"""View 层：将 ZJM 数据渲染为 HTML 页面。"""

from fastapi import Request
from fastapi.responses import HTMLResponse

from app.config.templates import templates
from app.models.zjm import ZjmItem


def render_zjm_page(request: Request, items: list[ZjmItem]) -> HTMLResponse:
    """数据列表 -> HTML 视图。"""
    return templates.TemplateResponse(
        request=request,
        name="zjm.html",
        context={"items": items},
    )
