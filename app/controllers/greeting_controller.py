"""Controller 层：接收请求、调用 Service、返回 View。"""

from fastapi import APIRouter, Path, Request
from fastapi.responses import HTMLResponse

from app.services.greeting_service import greeting_service
from app.views.greeting_page_view import render_greeting_page
from app.views.greeting_view import GreetingResponse

router = APIRouter(tags=["greeting"])


@router.get("/", response_model=GreetingResponse, summary="Hello World")
def hello() -> GreetingResponse:
    return GreetingResponse.from_model(greeting_service.greet())


@router.get("/hello/{name}", response_model=GreetingResponse, summary="带名字的问候")
def hello_name(name: str = Path(..., min_length=1, max_length=50, description="名字")) -> GreetingResponse:
    return GreetingResponse.from_model(greeting_service.greet(name))


@router.get("/page", response_class=HTMLResponse, summary="Hello World 页面")
def hello_page(request: Request) -> HTMLResponse:
    """HTML 视图，供浏览器直接访问。"""
    return render_greeting_page(request, greeting_service.greet())


@router.get("/page/hello/{name}", response_class=HTMLResponse, summary="带名字的问候页面")
def hello_page_name(
    request: Request,
    name: str = Path(..., min_length=1, max_length=50, description="名字"),
) -> HTMLResponse:
    return render_greeting_page(request, greeting_service.greet(name))
