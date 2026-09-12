"""数据模型 - 学习日志的结构定义"""

import uuid
from datetime import UTC, datetime

from pydantic import BaseModel, Field


def new_id() -> str:
    """生成唯一ID（uuid4 短版本）"""
    return uuid.uuid4().hex[:8]


class StudyLogCreate(BaseModel):
    """创建日志时客户端传来的数据（没有id和时间，服务器负责生成）"""

    title: str = Field(min_length=1, max_length=50, description="标题")
    content: str = Field(min_length=5, description="正文")
    tag: str | None = Field(default=None, description="标签，可选")
    minutes: int = Field(default=30, ge=0, le=1440, description="学习分钟数")


class StudyLog(BaseModel):
    """完整的一条日志（含id和创建时间，存进文件和返回给客户端用）"""

    id: str
    title: str
    content: str
    tag: str | None = None
    minutes: int = 30
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(timespec="seconds")
    )
