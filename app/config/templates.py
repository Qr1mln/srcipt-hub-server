"""Jinja2 模板环境（View 层渲染引擎）。"""

from pathlib import Path

from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "views" / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
