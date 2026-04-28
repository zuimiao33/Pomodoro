# 任务清单 + 番茄钟

在线任务清单与番茄钟应用。

## 技术栈

- 后端：FastAPI + SQLAlchemy 2.0 + Alembic
- 前端：Vue 3 + Vite + TypeScript
- 开发数据库：SQLite（`backend/todo.db`）

## 快速开始

1. 安装后端依赖

```bash
cd backend
python -m pip install -r requirements.txt
```

2. 安装前端依赖

```bash
cd frontend
npm install
```

3. 启动前后端服务

```bash
.\start-dev.cmd
```

4. 打开应用

- 前端页面：http://127.0.0.1:5173
- 后端文档：http://127.0.0.1:8000/docs
