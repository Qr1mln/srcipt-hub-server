"""Model 层：分类条目的领域模型。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryItem:
    """一条分类数据。

    字段名与接口约定保持一致：`id` 为数据库自增主键，`item` 为分类名称。
    """

    item: str
    id: int | None = None
