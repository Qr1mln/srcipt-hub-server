"""运行期状态：保存 uvicorn Server 实例，供接口触发优雅退出。

入口在启动前调用 bind_server()；热重载模式下应用跑在子进程里（模块状态不共享），
此时 request_shutdown() 返回 False，由接口提示用户改用 Ctrl+C 关闭。
"""

from typing import Any

_server: Any = None


def bind_server(server: Any) -> None:
    """绑定 uvicorn Server 实例。"""
    global _server
    _server = server


def request_shutdown() -> bool:
    """请求关闭服务，返回是否已发出关闭信号。"""
    if _server is None:
        return False
    _server.should_exit = True
    return True
