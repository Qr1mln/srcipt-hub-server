"""Service 层：登录校验与登录态令牌。"""

import base64
import binascii
import hashlib
import hmac
import json
import time

from app.config.config import ADMIN_PASSWORD, ADMIN_USERNAME, AUTH_SECRET, AUTH_TTL_SECONDS


class AuthService:
    """账号写死（config.ADMIN_USERNAME / ADMIN_PASSWORD），令牌用 HMAC 签名。"""

    def verify_credentials(self, username: str, password: str) -> bool:
        """校验账号密码，使用恒定时间比较避免时序泄漏。"""
        return hmac.compare_digest(username, ADMIN_USERNAME) and hmac.compare_digest(password, ADMIN_PASSWORD)

    def issue_token(self, username: str) -> str:
        """生成带过期时间的签名令牌：base64(payload).signature。"""
        payload = {"u": username, "e": int(time.time()) + AUTH_TTL_SECONDS}
        raw = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
        return f"{raw}.{self._sign(raw)}"

    def verify_token(self, token: str | None) -> str | None:
        """校验令牌，合法且未过期时返回用户名，否则返回 None。"""
        if not token or "." not in token:
            return None
        payload, _, signature = token.partition(".")
        if not hmac.compare_digest(signature, self._sign(payload)):
            return None
        try:
            data = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
            expires = int(data.get("e", 0))
        except (ValueError, TypeError, binascii.Error):
            return None
        if expires < time.time():
            return None
        username = str(data.get("u") or "")
        return username or None

    @staticmethod
    def _sign(payload: str) -> str:
        return hmac.new(AUTH_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()


auth_service = AuthService()
