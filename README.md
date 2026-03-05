# FastAPI + MySQL + Celery 示例项目

这是一个按子模块拆分路由的 FastAPI 项目，包含：

- `users` 子模块路由：用户创建与查询
- `items` 子模块路由：物品创建与查询
- `tasks` 子模块路由：触发 Celery 异步任务
- MySQL 数据库（SQLAlchemy）
- Celery 任务队列（默认 Redis 作为 broker/backend）
- Docker / Docker Compose 一键启动

## 项目结构

```text
app/
  api/
    users.py
    items.py
    tasks.py
  core/
    config.py
  db/
    base.py
    session.py
  models/
    user.py
    item.py
  schemas/
    user.py
    item.py
  tasks/
    celery_app.py
    jobs.py
  main.py
Dockerfile
docker-compose.yml
```

## 方式一：使用 Docker 运行（推荐）

### 1) 准备环境变量

```bash
cp .env.example .env
```

> 当前 `.env.example` 默认使用 Compose 内部网络主机名：`mysql`、`redis`。

### 2) 启动全部服务

```bash
docker compose up --build
```

启动后包含 4 个服务：

- `api`：FastAPI Web 服务（`http://localhost:8000`）
- `worker`：Celery Worker
- `mysql`：MySQL 8.0
- `redis`：Redis 7

### 3) 停止并清理

```bash
docker compose down
```

如需连同数据卷一起删除：

```bash
docker compose down -v
```

## 方式二：本地 Python 环境运行

### 1) 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) 配置环境变量

```bash
cp .env.example .env
```

如果你是本地安装 MySQL / Redis（非 Docker Compose），请把 `.env` 中：

- `MYSQL_HOST` 改成 `127.0.0.1`
- `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` 里的 `redis` 改成 `127.0.0.1`

### 3) 启动 FastAPI

```bash
uvicorn app.main:app --reload
```

### 4) 启动 Celery Worker

```bash
celery -A app.tasks.celery_app.celery_app worker -l info -Q default,emails
```

## 主要 API 路由

- `POST /api/v1/users/`：创建用户（成功后异步发送欢迎邮件任务）
- `GET /api/v1/users/`：查询用户列表
- `POST /api/v1/items/`：创建物品
- `GET /api/v1/items/`：查询物品列表
- `POST /api/v1/tasks/calculate/{value}`：触发异步计算任务
- `GET /docs`：Swagger 文档
