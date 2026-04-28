# 后端服务（FastAPI）

## 1. 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. 配置

复制 `.env.example` 为 `.env`，并填写数据库与 JWT 配置。

## 3. 启动

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Windows 也可以直接运行：

```bash
start-dev.cmd
```

## 4. Alembic 数据库迁移

```bash
alembic revision --autogenerate -m "init tables"
alembic upgrade head
```

## 5. OpenAPI 文档

- http://127.0.0.1:8000/docs
