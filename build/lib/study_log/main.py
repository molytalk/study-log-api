"""个人学习日志 API - 路由层"""

from fastapi import FastAPI, HTTPException

from . import storage
from .models import StudyLog, StudyLogCreate, new_id

app = FastAPI(title="个人学习日志 API", version="0.1.0")
storage._init_db()

@app.post("/logs", status_code=201)
def create_log(entry: StudyLogCreate):
    """创建一条学习日志"""
    full = StudyLog(id=new_id(), **entry.model_dump())
    saved = storage.create(full)
    return saved


@app.get("/logs/{log_id}")
def get_log(log_id: str):
    """根据日志ID获取日志"""
    log = storage.get_by_id(log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="日志不存在")
    return log

@app.get("/logs")
def list_logs(q: str | None = None):
    """列出全部学习日志（新的在前），可按关键词搜索"""
    if q is None:
        return storage.list_all()
    else:
        return storage.search(q)