"""Model 层：领域数据与业务规则，不感知 HTTP 与序列化细节。"""

from dataclasses import dataclass

DEFAULT_MESSAGE = "Hello World"


@dataclass(frozen=True)
class Greeting:
    """问候语领域模型。"""

    content: str

    @classmethod
    def world(cls) -> "Greeting":
        """默认问候。"""
        return cls(content=DEFAULT_MESSAGE)

    @classmethod
    def for_name(cls, name: str) -> "Greeting":
        """针对指定名字的问候。"""
        return cls(content=f"Hello, {name.strip()}!")
