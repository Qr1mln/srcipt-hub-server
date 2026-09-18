"""Service 层：ZJM 业务逻辑。"""

from app.models.zjm import ZjmItem
from app.repositories import zjm_repository


class InvalidZjmError(Exception):
    """zjm 或 str 为空。"""


class DuplicateZjmError(Exception):
    """zjm 已存在。"""


class NotFoundZjmError(Exception):
    """zjm 不存在。"""


class ZjmService:
    """ZJM 数据服务。"""

    def list_items(self) -> list[ZjmItem]:
        return zjm_repository.list_items()

    def add_item(self, zjm: str, text: str) -> ZjmItem:
        """新增数据：去空格、非空校验、唯一性校验。"""
        key = zjm.strip()
        value = text.strip()
        if not key or not value:
            raise InvalidZjmError("zjm 和 str 都不能为空")
        if zjm_repository.exists(key):
            raise DuplicateZjmError(f"zjm '{key}' 已存在")
        return zjm_repository.add_item(ZjmItem(zjm=key, str=value))

    def update_item(self, original_zjm: str, zjm: str, text: str) -> ZjmItem:
        """按原简称修改一条数据，允许同时改简称。"""
        key = zjm.strip()
        value = text.strip()
        if not key or not value:
            raise InvalidZjmError("zjm 和 str 都不能为空")
        if zjm_repository.get_item(original_zjm) is None:
            raise NotFoundZjmError(f"zjm '{original_zjm}' 不存在")
        if key != original_zjm and zjm_repository.exists(key):
            raise DuplicateZjmError(f"zjm '{key}' 已存在")
        return zjm_repository.update_item(original_zjm, ZjmItem(zjm=key, str=value))

    def delete_item(self, zjm: str) -> None:
        """删除一条数据，不存在则报错。"""
        if not zjm_repository.delete_item(zjm.strip()):
            raise NotFoundZjmError(f"zjm '{zjm}' 不存在")


zjm_service = ZjmService()
