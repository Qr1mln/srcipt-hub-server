# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller 打包配置（单文件 exe，控制台程序）。

构建：pyinstaller --noconfirm zjm_server.spec
产物：dist/zjm_server.exe，双击运行后访问 http://127.0.0.1:8000

要点：
- datas 把 Jinja2 模板打进包内，解包后路径为 app/views/templates（对应 app/config/templates.py）。
- hiddenimports 收集 uvicorn 的动态子模块（loops / protocols / lifespan）。
- 数据库由 app/config/config.py 的 data_dir() 定位到 exe 同级 data 目录，不会写进临时解包目录。
"""

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules('uvicorn')

# conda 环境把 OpenSSL / SQLite / libffi 等 DLL 放在 <env>/Library/bin，
# PyInstaller 默认找不到，运行时会报 "_ssl/_sqlite3 DLL load failed"，这里显式收集。
# 非 conda 环境（python.org 安装）该目录不存在，对应 DLL 会被 PyInstaller 自动解析。
binaries = []
_conda_bin = Path(sys.prefix) / "Library" / "bin"
if _conda_bin.is_dir():
    for _pattern in (
        "sqlite3.dll",
        "libssl-*.dll",
        "libcrypto-*.dll",
        "ffi*.dll",
        "libexpat.dll",
        "zlib.dll",
        "liblzma.dll",
        "libbz2.dll",
    ):
        binaries += [(str(_dll), ".") for _dll in _conda_bin.glob(_pattern)]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=[('app/views/templates', 'app/views/templates')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='zjm_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
