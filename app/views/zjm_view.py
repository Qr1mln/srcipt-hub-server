"""View 层：ZJM 接口的请求/响应结构。

注意：由于业务字段名就叫 `str`，其元数据必须用 `Annotated[str, Field(...)]` 写法，
写成 `str: str = Field(...)` 会被 Pydantic 判定为「字段名与类型注解冲突」而报错。
"""

from typing import Annotated

from pydantic import BaseModel, Field

from app.models.zjm import ZjmItem


class ZjmItemView(BaseModel):
    """单条 ZJM 数据。"""

    zjm: Annotated[str, Field(description="简称", examples=["qcxs"])]
    str: Annotated[str, Field(description="描述", examples=["起床洗漱。"])]

    @classmethod
    def from_model(cls, model: ZjmItem) -> "ZjmItemView":
        return cls(zjm=model.zjm, str=model.str)


class ZjmResponse(BaseModel):
    """统一响应格式：{code, body, msg}。"""

    code: Annotated[int, Field(description="业务状态码，200 表示成功")] = 200
    body: Annotated[list[ZjmItemView], Field(description="数据列表")] = Field(default_factory=list)
    msg: Annotated[str, Field(description="提示信息")] = "success"

    @classmethod
    def ok(cls, items: list[ZjmItem], msg: str = "success") -> "ZjmResponse":
        return cls(
            code=200,
            body=[ZjmItemView.from_model(item) for item in items],
            msg=msg,
        )

    @classmethod
    def fail(cls, code: int, msg: str) -> "ZjmResponse":
        return cls(code=code, body=[], msg=msg)


class ZjmSaveRequest(BaseModel):
    """新增/修改请求体（修改时 path 中的 zjm 为原简称）。"""

    zjm: Annotated[str, Field(min_length=1, max_length=32, description="简称")]
    str: Annotated[str, Field(min_length=1, max_length=200, description="描述")]
