"""Model 层：ZJM 条目的领域模型。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ZjmItem:
    """一条 ZJM 数据。

    字段名与接口约定保持一致，`str` 为业务字段（描述），不是内建类型。
    """

    zjm: str
    str: str
