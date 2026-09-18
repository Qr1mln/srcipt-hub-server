"""View 层：将领域模型渲染为 HTML 页面。"""

from fastapi import Request
from fastapi.responses import HTMLResponse

from app.config.templates import templates
from app.models.greeting import Greeting


def render_greeting_page(request: Request, greeting: Greeting) -> HTMLResponse:
    """领域模型 -> HTML 视图。"""
    return templates.TemplateResponse(
        request=request,
        name="greeting.html",
        context={"message": greeting.content},
    )
