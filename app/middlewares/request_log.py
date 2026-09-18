"""中间件：请求日志。"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("zjm.request")


def _target(request: Request) -> str:
    """请求路径（含查询串）。"""
    query = request.url.query
    return f"{request.url.path}?{query}" if query else request.url.path


def _client(request: Request) -> str:
    """客户端地址:端口，取不到时为 "-"。"""
    client = request.client
    return f"{client.host}:{client.port}" if client is not None else "-"


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """记录每次请求：方法、路径、状态码、耗时、客户端地址。

    状态码 <400 记 INFO，4xx 记 WARNING，5xx 或异常记 ERROR（异常时带堆栈）。
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "%s %s | 异常 | %.1fms | %s",
                request.method,
                _target(request),
                (time.perf_counter() - start) * 1000,
                _client(request),
            )
            raise

        cost = (time.perf_counter() - start) * 1000
        args = (request.method, _target(request), response.status_code, cost, _client(request))
        message = "%s %s | %s | %.1fms | %s"
        if response.status_code >= 500:
            logger.error(message, *args)
        elif response.status_code >= 400:
            logger.warning(message, *args)
        else:
            logger.info(message, *args)
        return response
