"""Repository 层：分类的 SQLite 持久化。"""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager

from app.config.config import settings
from app.models.category import CategoryItem

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL UNIQUE
)
"""

# 首次建库时的初始数据
DEFAULT_ITEMS: tuple[str, ...] = (
    "生活日常",
    "工作事务",
    "学习笔记",
)


@contextmanager
def _connection() -> Iterator[sqlite3.Connection]:
    """打开连接，正常退出时提交，最后关闭。"""
    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(settings.db_path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def _to_model(row: sqlite3.Row) -> CategoryItem:
    return CategoryItem(id=row["id"], item=row["item"])


def init_db(seed: bool = True) -> None:
    """建表；表为空时写入初始数据。"""
    with _connection() as connection:
        connection.execute(CREATE_TABLE_SQL)
        if seed and connection.execute("SELECT COUNT(*) FROM categories").fetchone()[0] == 0:
            connection.executemany(
                "INSERT INTO categories (item) VALUES (?)",
                [(item,) for item in DEFAULT_ITEMS],
            )


def list_items() -> list[CategoryItem]:
    """按 id 顺序返回全部分类。"""
    with _connection() as connection:
        rows = connection.execute("SELECT id, item FROM categories ORDER BY id").fetchall()
    return [_to_model(row) for row in rows]


def exists(item: str) -> bool:
    with _connection() as connection:
        row = connection.execute("SELECT 1 FROM categories WHERE item = ?", (item,)).fetchone()
    return row is not None


def find_by_item(item: str) -> CategoryItem | None:
    """按名称查询单条，用于改名时判断是否撞上其它记录。"""
    with _connection() as connection:
        row = connection.execute("SELECT id, item FROM categories WHERE item = ?", (item,)).fetchone()
    return _to_model(row) if row is not None else None


def add_item(item: CategoryItem) -> CategoryItem:
    """新增一条分类并返回带自增 id 的记录。"""
    with _connection() as connection:
        cursor = connection.execute("INSERT INTO categories (item) VALUES (?)", (item.item,))
        new_id = cursor.lastrowid
    return CategoryItem(id=new_id, item=item.item)


def get_item(category_id: int) -> CategoryItem | None:
    """按 id 查询单条，不存在返回 None。"""
    with _connection() as connection:
        row = connection.execute(
            "SELECT id, item FROM categories WHERE id = ?", (category_id,)
        ).fetchone()
    return _to_model(row) if row is not None else None


def update_item(category_id: int, item: CategoryItem) -> CategoryItem:
    """按 id 更新分类名称。"""
    with _connection() as connection:
        connection.execute(
            "UPDATE categories SET item = ? WHERE id = ?",
            (item.item, category_id),
        )
    return CategoryItem(id=category_id, item=item.item)


def delete_item(category_id: int) -> bool:
    """删除成功返回 True。"""
    with _connection() as connection:
        cursor = connection.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    return cursor.rowcount > 0
