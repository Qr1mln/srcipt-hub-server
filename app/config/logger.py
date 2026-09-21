"""日志配置：控制台彩色输出（colorama）+ 滚动文件（logs/app.log，纯文本）。

颜色只在控制台处理器上生效；写文件时由 colorama 包装的流自动剥离 ANSI 转义符，
因此日志文件始终是纯文本。开关见 config.LOG_COLOR_ENABLED。
"""

import logging
from logging.handlers import RotatingFileHandler

from colorama import Fore, Style, init as colorama_init

from app.config.config import LOG_COLOR_ENABLED, base_dir

LOG_DIR = base_dir() / "logs"
LOG_FILE = LOG_DIR / "app.log"
LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_BYTES = 2 * 1024 * 1024
BACKUP_COUNT = 3

RESET = Style.RESET_ALL
GREY = Fore.LIGHTBLACK_EX

# 各级别对应的颜色
LEVEL_COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA,
}


class ColorFormatter(logging.Formatter):
    """控制台彩色格式：级别与消息按等级着色，时间、模块名置灰。"""

    def format(self, record: logging.LogRecord) -> str:
        color = LEVEL_COLORS.get(record.levelno, "")
        text = (
            f"{GREY}{self.formatTime(record, DATE_FORMAT)}{RESET} | "
            f"{color}{record.levelname:<7}{RESET} | "
            f"{GREY}{record.name}{RESET} | "
            f"{color}{record.getMessage()}{RESET}"
        )
        if record.exc_info:
            text = f"{text}\n{self.formatException(record.exc_info)}"
        elif record.exc_text:
            text = f"{text}\n{record.exc_text}"
        return text


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """初始化根日志：控制台（彩色）+ 滚动文件（纯文本）；重复调用不会重复添加 handler。"""
    # 降低第三方库噪声（watchfiles 每次文件变化都会打 INFO；httpx 是测试客户端）
    for noisy in ("watchfiles", "watchfiles.main", "httpx", "httpx2", "httpcore", "httpcore2"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    root = logging.getLogger()
    if any(isinstance(handler, RotatingFileHandler) for handler in root.handlers):
        return root
    root.setLevel(level)

    # Windows 下开启 ANSI 支持，并包装 stdout/stderr（写到非终端时自动剥离颜色）
    colorama_init(autoreset=True)

    console = logging.StreamHandler()
    console.setFormatter(
        ColorFormatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
        if LOG_COLOR_ENABLED
        else logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    )
    root.addHandler(console)

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
        root.addHandler(file_handler)
    except OSError:
        # 目录不可写时仅输出到控制台，不影响服务启动
        root.warning("日志文件不可写，已跳过文件日志：%s", LOG_FILE)
    return root
