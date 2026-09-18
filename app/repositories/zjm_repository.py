"""Repository 层：ZJM 条目的 SQLite 持久化。"""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager

from app.config.config import settings
from app.models.zjm import ZjmItem

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS zjm (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    zjm        TEXT NOT NULL UNIQUE,
    str        TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
)
"""

# 首次建库时的初始数据
DEFAULT_ITEMS: tuple[tuple[str, str], ...] = (
    ("qcxs", "起床洗漱。"),
    ("czc", "吃早餐。"),
    ("ssp", " 刷视频。"),
    ("hxb", "还行吧。"),
    ("cwf", "吃晚饭。"),
    ("kdm", "看动漫。"),
    ("cwc", "吃午餐。"),
    ("yyj", "养眼睛。"),
    ("fcbc", "非常不错。"),
    ("cqsb", "出去散步。"),
    ("yhyhjb", "优化用户脚本。"),
    ("whjzg", "玩火炬之光。"),
    ("wsjz", "玩三角洲。"),
    ("xssj", "洗漱睡觉。"),
    ("wwzry", "玩王者荣耀。"),
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


def _to_model(row: sqlite3.Row) -> ZjmItem:
    return ZjmItem(zjm=row["zjm"], str=row["str"])


def init_db(seed: bool = True) -> None:
    """建表；表为空时写入初始数据。"""
    with _connection() as connection:
        connection.execute(CREATE_TABLE_SQL)
        if seed and connection.execute("SELECT COUNT(*) FROM zjm").fetchone()[0] == 0:
            connection.executemany("INSERT INTO zjm (zjm, str) VALUES (?, ?)", DEFAULT_ITEMS)


def list_items() -> list[ZjmItem]:
    """按写入顺序返回全部数据。"""
    with _connection() as connection:
        rows = connection.execute("SELECT zjm, str FROM zjm ORDER BY id").fetchall()
    return [_to_model(row) for row in rows]


def exists(zjm: str) -> bool:
    with _connection() as connection:
        row = connection.execute("SELECT 1 FROM zjm WHERE zjm = ?", (zjm,)).fetchone()
    return row is not None


def add_item(item: ZjmItem) -> ZjmItem:
    """新增一条数据并返回。"""
    with _connection() as connection:
        connection.execute("INSERT INTO zjm (zjm, str) VALUES (?, ?)", (item.zjm, item.str))
    return item


def get_item(zjm: str) -> ZjmItem | None:
    """按简称查询单条，不存在返回 None。"""
    with _connection() as connection:
        row = connection.execute("SELECT zjm, str FROM zjm WHERE zjm = ?", (zjm,)).fetchone()
    return _to_model(row) if row is not None else None


def update_item(original_zjm: str, item: ZjmItem) -> ZjmItem:
    """按原简称更新，允许同时修改简称。"""
    with _connection() as connection:
        connection.execute(
            "UPDATE zjm SET zjm = ?, str = ? WHERE zjm = ?",
            (item.zjm, item.str, original_zjm),
        )
    return item


def delete_item(zjm: str) -> bool:
    """删除成功返回 True。"""
    with _connection() as connection:
        cursor = connection.execute("DELETE FROM zjm WHERE zjm = ?", (zjm,))
    return cursor.rowcount > 0
