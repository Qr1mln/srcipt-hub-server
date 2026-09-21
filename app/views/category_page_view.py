"""View 层：将分类数据渲染为 HTML 页面。"""

from fastapi import Request
from fastapi.responses import HTMLResponse

from app.config.templates import templates
from app.models.category import CategoryItem


def render_category_page(request: Request, items: list[CategoryItem]) -> HTMLResponse:
    """分类列表 -> HTML 视图。"""
    return templates.TemplateResponse(
        request=request,
        name="categories.html",
        context={"items": items},
    )
