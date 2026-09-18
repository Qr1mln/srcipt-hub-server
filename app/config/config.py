"""全局配置。"""


class Settings:
    """应用配置项，后续可替换为 pydantic-settings 读取环境变量。"""

    app_name: str = "Hello World Demo"
    version: str = "0.1.0"
    description: str = "FastAPI MVC 架构示例"


settings = Settings()
