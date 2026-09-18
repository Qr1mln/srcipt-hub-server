"""Service 层：编排领域逻辑，供 Controller 调用。"""

from app.models.greeting import Greeting


class GreetingService:
    """问候业务服务。"""

    def greet(self, name: str | None = None) -> Greeting:
        """name 为空时返回默认问候。"""
        if name is None or not name.strip():
            return Greeting.world()
        return Greeting.for_name(name)


greeting_service = GreetingService()
