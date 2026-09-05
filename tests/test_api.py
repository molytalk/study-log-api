"""学习日志 API 的自动化测试"""

import pytest
from fastapi.testclient import TestClient

from study_log import storage
from study_log.main import app


# TestClient: 在内存里跑应用，不占真实端口
@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def clean_db(tmp_path, monkeypatch):
    """在测试前创建一个临时数据库文件，测试后删除"""
    test_db_file = tmp_path / "test.db"
    monkeypatch.setattr(storage, "DB_FILE", test_db_file)
    storage._init_db()
    yield test_db_file


def test_create_log(client, clean_db):
    """创建一条日志，应返回 201 和自动生成的 id"""
    resp = client.post("/logs", json={"title": "测试标题", "content": "这是一条足够长的测试内容", "minutes": 45})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "测试标题"
    assert data["id"]  # id 非空


def test_list_logs(client, clean_db):
    """列表接口应返回数组（每条都有 id）"""
    resp = client.get("/logs")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_validation_error(client, clean_db):
    """内容太短应被 Pydantic 拦下，返回 422 而不是 500"""
    resp = client.post("/logs", json={"title": "", "content": "ab"})
    assert resp.status_code == 422


def test_get_nonexistent(client, clean_db):
    """查不存在的 id 应返回 404"""
    resp = client.get("/logs/not-exist-123")
    assert resp.status_code == 404

def test_search(client, clean_db):
    """搜索接口应返回包含关键词的日志"""
    resp = client.post("/logs", json={"title": "Python_Learning", "content": "这是一条关于 Python 学习的日志", "minutes": 45})
    resp = client.get("/logs?q=python")
    assert len(resp.json()) == 1


def test_get_by_id(client, clean_db):
    """根据日志ID获取日志"""
    resp = client.post("/logs", json={"title": "按照id查找", "content": "这是一条关于学习fixture的日志", "minutes": 45})
    data = resp.json()
    resp = client.get(f"/logs/{data['id']}")
    assert resp.status_code == 200
