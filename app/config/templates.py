"""Jinja2 模板环境（View 层渲染引擎）。"""

from fastapi.templating import Jinja2Templates

from app.config.config import resource_dir

# 打包后模板位于解包目录的 app/views/templates（见 zjm_server.spec 的 datas）
TEMPLATES_DIR = resource_dir() / "app" / "views" / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
