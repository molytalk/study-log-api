"""数据层 - 学习日志的持久化存储（SQLite 版）"""
import sqlite3
from pathlib import Path

from .models import StudyLog

# 数据库文件路径，默认在项目根目录下的 logs.db，resolve() 确保路径是绝对的
DB_FILE = Path(__file__).resolve().parent.parent.parent / "logs.db"

def _get_conn():
    """获取数据库连接（row_factory 让结果能按字段名取值）"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def _init_db():
    """建表（程序启动时调用一次，IF NOT EXISTS 保证幂等）"""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tag TEXT,
                minutes INTEGER DEFAULT 30,
                created_at TEXT
            )
        """)




def create(entry: StudyLog) -> StudyLog:
    """新增一条日志，返回带id的完整日志"""
    # 确保连接存在，数据表存在
    with _get_conn() as conn: 
        conn.execute("INSERT INTO logs (id, title, content, tag, minutes, created_at)VALUES (?, ?, ?, ?, ?, ?)",
                    (entry.id, entry.title, entry.content, entry.tag, entry.minutes, entry.created_at))
        conn.commit()
    return entry


def list_all() -> list[StudyLog]:
    """返回全部日志，按创建时间倒序（最新的在前）"""
    with _get_conn() as conn:
        cursor = conn.execute("SELECT * FROM logs ORDER BY created_at DESC")
        return [StudyLog(**dict(item)) for item in cursor.fetchall()]


def get_by_id(log_id: str) -> StudyLog | None:
    """根据日志ID获取日志，找不到返回 None"""
    with _get_conn() as conn:
        cursor = conn.execute("SELECT * FROM logs WHERE id = ?", (log_id,))
    row = cursor.fetchone()
    if row :
        return StudyLog(**dict(row))
    return None


def search(keyword: str) -> list[StudyLog]:
    """按关键词搜索：标题/内容/标签 任一包含即命中，不区分大小写"""
    with _get_conn() as conn:
        cursor = conn.execute("""
            SELECT * FROM logs
            WHERE lower(title) LIKE lower('%' || ? || '%') OR lower(content) LIKE lower('%' || ? || '%') OR lower(tag) LIKE lower('%' || ? || '%')
            ORDER BY created_at DESC
        """, (keyword, keyword, keyword))
    return [StudyLog(**dict(item)) for item in cursor.fetchall()]
    
