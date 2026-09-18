"""View 层：登录接口的请求/响应结构。"""

from typing import Annotated

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求体。"""

    username: Annotated[str, Field(min_length=1, max_length=32, description="账号")]
    password: Annotated[str, Field(min_length=1, max_length=32, description="密码")]


class LoginInfo(BaseModel):
    """登录成功信息。"""

    username: Annotated[str, Field(description="登录账号")]
    redirect: Annotated[str, Field(description="登录后跳转地址")] = "/"


class LoginResponse(BaseModel):
    """登录响应，沿用统一格式 {code, body, msg}；401 表示账号或密码错误。"""

    code: Annotated[int, Field(description="业务状态码，200 成功 / 401 账号或密码错误")] = 200
    body: Annotated[list[LoginInfo], Field(description="登录信息")] = Field(default_factory=list)
    msg: Annotated[str, Field(description="提示信息")] = "success"


class SimpleResponse(BaseModel):
    """无数据返回的统一响应（body 恒为空列表）。"""

    code: Annotated[int, Field(description="业务状态码，200 表示成功")] = 200
    body: Annotated[list[LoginInfo], Field(description="数据列表，此处恒为空")] = Field(default_factory=list)
    msg: Annotated[str, Field(description="提示信息")] = "success"

    @classmethod
    def ok(cls, msg: str = "success") -> "SimpleResponse":
        return cls(code=200, body=[], msg=msg)

    @classmethod
    def fail(cls, code: int, msg: str) -> "SimpleResponse":
        return cls(code=code, body=[], msg=msg)
