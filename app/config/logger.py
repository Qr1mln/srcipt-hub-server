"""日志配置：控制台 + 滚动文件（logs/app.log）。"""

import logging
from logging.handlers import RotatingFileHandler

from app.config.config import base_dir

LOG_DIR = base_dir() / "logs"
LOG_FILE = LOG_DIR / "app.log"
LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_BYTES = 2 * 1024 * 1024
BACKUP_COUNT = 3


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """初始化根日志：控制台 + 滚动文件；重复调用不会重复添加 handler。"""
    # 降低第三方库噪声（watchfiles 每次文件变化都会打 INFO）
    for noisy in ("watchfiles", "watchfiles.main"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    root = logging.getLogger()
    if any(isinstance(handler, RotatingFileHandler) for handler in root.handlers):
        return root
    root.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
    except OSError:
        # 目录不可写时仅输出到控制台，不影响服务启动
        root.warning("日志文件不可写，已跳过文件日志：%s", LOG_FILE)
    return root
