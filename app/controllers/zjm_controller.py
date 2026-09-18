"""Controller 层：ZJM 接口路由。"""

from fastapi import APIRouter, Path, Request
from fastapi.responses import HTMLResponse

from app.services.zjm_service import (
    DuplicateZjmError,
    InvalidZjmError,
    NotFoundZjmError,
    zjm_service,
)
from app.views.zjm_page_view import render_zjm_page
from app.views.zjm_view import ZjmResponse, ZjmSaveRequest

router = APIRouter(tags=["zjm"])

# 业务异常 -> 统一响应 code
BUSINESS_ERRORS = (InvalidZjmError, DuplicateZjmError, NotFoundZjmError)
ERROR_CODES = {
    InvalidZjmError: 400,
    NotFoundZjmError: 404,
    DuplicateZjmError: 409,
}

ZjmPath = Path(..., min_length=1, max_length=32, description="简称")


def _fail(exc: Exception) -> ZjmResponse:
    return ZjmResponse.fail(ERROR_CODES.get(type(exc), 500), str(exc))


@router.get("/admin", response_class=HTMLResponse, summary="数据管理页（需登录）", include_in_schema=False)
def zjm_page(request: Request) -> HTMLResponse:
    """管理页面：展示列表，支持动态增、改、删。"""
    return render_zjm_page(request, zjm_service.list_items())


@router.get("/api/zjm", response_model=ZjmResponse, summary="查询全部 ZJM 数据")
def list_zjm() -> ZjmResponse:
    return ZjmResponse.ok(zjm_service.list_items())


@router.post("/api/zjm", response_model=ZjmResponse, summary="新增一条 ZJM 数据")
def add_zjm(payload: ZjmSaveRequest) -> ZjmResponse:
    try:
        item = zjm_service.add_item(payload.zjm, payload.str)
    except BUSINESS_ERRORS as exc:
        return _fail(exc)
    return ZjmResponse.ok([item])


@router.put("/api/zjm/{zjm}", response_model=ZjmResponse, summary="修改一条 ZJM 数据")
def update_zjm(payload: ZjmSaveRequest, zjm: str = ZjmPath) -> ZjmResponse:
    """path 传原简称，body 中的 zjm 为修改后的简称（可与原值相同）。"""
    try:
        item = zjm_service.update_item(zjm, payload.zjm, payload.str)
    except BUSINESS_ERRORS as exc:
        return _fail(exc)
    return ZjmResponse.ok([item])


@router.delete("/api/zjm/{zjm}", response_model=ZjmResponse, summary="删除一条 ZJM 数据")
def delete_zjm(zjm: str = ZjmPath) -> ZjmResponse:
    try:
        zjm_service.delete_item(zjm)
    except BUSINESS_ERRORS as exc:
        return _fail(exc)
    return ZjmResponse.ok([], msg="success")
