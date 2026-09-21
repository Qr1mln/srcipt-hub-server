"""Controller 层：分类接口路由。"""

from fastapi import APIRouter, Path, Request
from fastapi.responses import HTMLResponse

from app.services.category_service import (
    DuplicateCategoryError,
    InvalidCategoryError,
    NotFoundCategoryError,
    category_service,
)
from app.views.category_page_view import render_category_page
from app.views.category_view import CategoryResponse, CategorySaveRequest

router = APIRouter(tags=["categories"])

# 业务异常 -> 统一响应 code
BUSINESS_ERRORS = (InvalidCategoryError, DuplicateCategoryError, NotFoundCategoryError)
ERROR_CODES = {
    InvalidCategoryError: 400,
    NotFoundCategoryError: 404,
    DuplicateCategoryError: 409,
}

CategoryIdPath = Path(..., description="分类 ID")


def _fail(exc: Exception) -> CategoryResponse:
    return CategoryResponse.fail(ERROR_CODES.get(type(exc), 500), str(exc))


@router.get("/categories", response_class=HTMLResponse, summary="分类管理页（需登录）", include_in_schema=False)
def category_page(request: Request) -> HTMLResponse:
    """管理页面：展示列表，支持动态增、改、删。"""
    return render_category_page(request, category_service.list_items())


@router.get("/api/categories", response_model=CategoryResponse, summary="查询全部分类")
def list_categories() -> CategoryResponse:
    return CategoryResponse.ok(category_service.list_items())


@router.post("/api/categories", response_model=CategoryResponse, summary="新增一条分类")
def add_category(payload: CategorySaveRequest) -> CategoryResponse:
    try:
        item = category_service.add_item(payload.item)
    except BUSINESS_ERRORS as exc:
        return _fail(exc)
    return CategoryResponse.ok([item])


@router.put("/api/categories/{category_id}", response_model=CategoryResponse, summary="修改一条分类")
def update_category(payload: CategorySaveRequest, category_id: int = CategoryIdPath) -> CategoryResponse:
    try:
        item = category_service.update_item(category_id, payload.item)
    except BUSINESS_ERRORS as exc:
        return _fail(exc)
    return CategoryResponse.ok([item])


@router.delete("/api/categories/{category_id}", response_model=CategoryResponse, summary="删除一条分类")
def delete_category(category_id: int = CategoryIdPath) -> CategoryResponse:
    try:
        category_service.delete_item(category_id)
    except BUSINESS_ERRORS as exc:
        return _fail(exc)
    return CategoryResponse.ok([], msg="success")
