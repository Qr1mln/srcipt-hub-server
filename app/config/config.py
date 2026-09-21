"""全局配置。

路径策略（兼容源码运行与 PyInstaller 打包）：
- 静态资源（模板）：打包后位于解包目录 `sys._MEIPASS`，通过 `resource_dir()` 定位。
- SQLite 数据：放在 exe 同级目录（源码运行为项目根），见 `data_dir()`。

服务监听地址由命令行参数决定（`--host` / `--port`，见 main.py 的 parse_args），默认值见下。
"""

import sys
from pathlib import Path

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

# 允许跨域的来源；["*"] 表示不限制来源（需要收紧时改成具体域名列表）
DEFAULT_CORS_ORIGINS = ["*"]

# 登录账号（写死，本地工具用）
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"

# 控制台日志是否着色（文件日志始终为纯文本）
LOG_COLOR_ENABLED = True

# 登录态 Cookie（HMAC 签名，无需额外依赖）
AUTH_COOKIE = "zjm_token"
AUTH_SECRET = "zjm-server-local-secret"
AUTH_TTL_SECONDS = 12 * 3600


def is_frozen() -> bool:
    """是否运行在 PyInstaller 打包后的环境中。"""
    return getattr(sys, "frozen", False)


def project_root() -> Path:
    """源码运行时的项目根目录（app/config/config.py -> 上溯三层）。"""
    return Path(__file__).resolve().parent.parent.parent


def base_dir() -> Path:
    """可写文件基准目录：打包后为 exe 同级目录，源码运行为项目根。"""
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return project_root()


def resource_dir() -> Path:
    """静态资源根目录：打包后为解包目录，源码运行为项目根。"""
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS", base_dir()))
    return project_root()


def data_dir() -> Path:
    """SQLite 数据目录。"""
    return base_dir() / "data"


class Settings:
    """应用配置项（常量与路径）。"""

    app_name: str = "ZJM Server"
    version: str = "0.2.0"
    description: str = "ZJM 数据接口（统一响应格式，SQLite 存储）"

    # SQLite 数据库文件路径
    db_path: Path = data_dir() / "zjm.db"


settings = Settings()
