# Study Log API 📝

个人学习日志 API —— 记录每天学到的知识点，支持创建、列表、搜索、按 ID 查询。

这是 AI 学习路线 P1 工程基础阶段的实战项目：从零搭建一个**分层架构**的 FastAPI 服务，数据层经历 JSON → SQLite 迁移，并配有完整的自动化测试。

## 功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/logs` | 创建一条学习日志，返回 201 与自动生成的 id |
| `GET` | `/logs` | 列出全部日志（按创建时间倒序） |
| `GET` | `/logs?q=关键词` | 按关键词搜索（标题/内容/标签，不区分大小写） |
| `GET` | `/logs/{log_id}` | 按 ID 查询单条，不存在返回 404 |

交互式文档：启动后访问 `http://127.0.0.1:8002/docs`

## 技术栈

- **FastAPI** —— Web 框架，自动生成交互式 API 文档
- **Pydantic** —— 请求数据校验（长度、范围、可选字段）
- **SQLite** —— 零配置单文件数据库
- **pytest** + **TestClient** —— 自动化测试（6 个用例）
- **uv** —— 依赖与虚拟环境管理

## 快速开始

```bash
# 1. 创建虚拟环境并安装依赖
uv venv
uv pip install -e .

# 2. 启动服务
.venv/Scripts/python -m uvicorn study_log.main:app --port 8002

# 3. 试试接口
curl -X POST http://127.0.0.1:8002/logs \
  -H "Content-Type: application/json" \
  -d '{"title":"FastAPI","content":"学会写第一个接口","tag":"基础","minutes":60}'

curl http://127.0.0.1:8002/logs
curl "http://127.0.0.1:8002/logs?q=FastAPI"
```

## 运行测试

```bash
.venv/Scripts/python -m pytest tests/ -v
```

测试使用 `tmp_path` + `monkeypatch` 夹具隔离数据库，**不会污染真实的 `logs.db`**。

## 项目结构

```
study-log-api/
├── src/study_log/
│   ├── __init__.py
│   ├── main.py       # 路由层：HTTP 接口定义
│   ├── models.py     # 数据模型：Pydantic 校验规则
│   └── storage.py    # 数据层：SQLite 读写（分层核心）
├── tests/
│   └── test_api.py   # 6 个 API 测试
├── pyproject.toml    # 项目与依赖声明
└── uv.lock           # 依赖版本锁定
```

**分层设计**：路由层只管"对外长什么样"，数据层只管"数据存哪"。因此从 JSON 迁移到 SQLite 时，`main.py` 一行未改。

## 开发历程（学习轨迹）

- **T006**：JSON 文件存储 + 基础 CRUD
- **T007**：数据层迁移到 SQLite（不改路由层）
- **T008**：pytest 自动化测试 + fixture 数据库隔离
- **T009**：ruff 规范检查（含 UTC 时区修复）、Git 版本管理、部署到 GitHub
