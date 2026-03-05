# FastAPI + MySQL + Celery 示例项目

这是一个按子模块拆分路由的 FastAPI 项目，包含：

- `users` 子模块路由：用户创建与查询
- `items` 子模块路由：物品创建与查询
- `tasks` 子模块路由：触发 Celery 异步任务
- MySQL 数据库（SQLAlchemy）
- Celery 任务队列（默认 Redis 作为 broker/backend）

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
```

## 1. 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. 配置环境变量

```bash
cp .env.example .env
```

根据你的本机环境修改 `.env` 中的 MySQL 和 Redis 连接配置。

## 3. 启动 FastAPI

```bash
uvicorn app.main:app --reload
```

访问：

- 首页健康检查：`GET /`
- OpenAPI 文档：`GET /docs`

## 4. 启动 Celery Worker

```bash
celery -A app.tasks.celery_app.celery_app worker -l info -Q default,emails
```

## 5. 主要 API 路由

- `POST /api/v1/users/`：创建用户（成功后异步发送欢迎邮件任务）
- `GET /api/v1/users/`：查询用户列表
- `POST /api/v1/items/`：创建物品
- `GET /api/v1/items/`：查询物品列表
- `POST /api/v1/tasks/calculate/{value}`：触发异步计算任务
