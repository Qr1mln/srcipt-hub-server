"""Service 层：分类业务逻辑。"""

from app.models.category import CategoryItem
from app.repositories import category_repository


class InvalidCategoryError(Exception):
    """item 为空。"""


class DuplicateCategoryError(Exception):
    """分类名称已存在。"""


class NotFoundCategoryError(Exception):
    """分类不存在。"""


class CategoryService:
    """分类数据服务。"""

    def list_items(self) -> list[CategoryItem]:
        return category_repository.list_items()

    def add_item(self, item: str) -> CategoryItem:
        """新增分类：去空格、非空校验、唯一性校验。"""
        value = item.strip()
        if not value:
            raise InvalidCategoryError("item 不能为空")
        if category_repository.exists(value):
            raise DuplicateCategoryError(f"分类 '{value}' 已存在")
        return category_repository.add_item(CategoryItem(item=value))

    def update_item(self, category_id: int, item: str) -> CategoryItem:
        """按 id 修改一条分类的名称，允许改名但不与已有分类重名。"""
        value = item.strip()
        if not value:
            raise InvalidCategoryError("item 不能为空")
        if category_repository.get_item(category_id) is None:
            raise NotFoundCategoryError(f"id {category_id} 的分类不存在")
        conflict = category_repository.find_by_item(value)
        if conflict is not None and conflict.id != category_id:
            raise DuplicateCategoryError(f"分类 '{value}' 已存在")
        return category_repository.update_item(category_id, CategoryItem(item=value))

    def delete_item(self, category_id: int) -> None:
        """删除一条分类，不存在则报错。"""
        if not category_repository.delete_item(category_id):
            raise NotFoundCategoryError(f"id {category_id} 的分类不存在")


category_service = CategoryService()
