"""View 层：对外暴露的请求/响应结构（Pydantic schema）。"""

from pydantic import BaseModel, Field

from app.models.greeting import Greeting


class GreetingResponse(BaseModel):
    """问候接口响应体。"""

    message: str = Field(..., description="问候语", examples=["Hello World"])

    @classmethod
    def from_model(cls, model: Greeting) -> "GreetingResponse":
        """领域模型 -> 响应视图。"""
        return cls(message=model.content)
