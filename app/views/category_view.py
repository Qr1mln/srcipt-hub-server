"""View 层：分类接口的请求/响应结构。"""

from typing import Annotated

from pydantic import BaseModel, Field

from app.models.category import CategoryItem


class CategoryItemView(BaseModel):
    """单条分类数据；id 以字符串形式返回，与接口约定一致。"""

    id: Annotated[str, Field(description="分类 ID")]
    item: Annotated[str, Field(description="分类名称")]

    @classmethod
    def from_model(cls, model: CategoryItem) -> "CategoryItemView":
        return cls(id=str(model.id), item=model.item)


class CategoryResponse(BaseModel):
    """统一响应格式：{code, body, msg}。"""

    code: Annotated[int, Field(description="业务状态码，200 表示成功")] = 200
    body: Annotated[list[CategoryItemView], Field(description="数据列表")] = Field(default_factory=list)
    msg: Annotated[str, Field(description="提示信息")] = "success"

    @classmethod
    def ok(cls, items: list[CategoryItem], msg: str = "success") -> "CategoryResponse":
        return cls(
            code=200,
            body=[CategoryItemView.from_model(item) for item in items],
            msg=msg,
        )

    @classmethod
    def fail(cls, code: int, msg: str) -> "CategoryResponse":
        return cls(code=code, body=[], msg=msg)


class CategorySaveRequest(BaseModel):
    """新增/修改请求体。"""

    item: Annotated[str, Field(min_length=1, max_length=100, description="分类名称")]
