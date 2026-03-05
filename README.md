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

### 2) 按你的场景启动

#### 场景 A：MySQL/Redis 在其他 Linux 服务器（你的场景）

把 `.env` 改成外部地址，例如：

```env
MYSQL_HOST="10.10.10.20"
MYSQL_PORT=3306
MYSQL_USER="your_user"
MYSQL_PASSWORD="your_password"
MYSQL_DB="your_db"

CELERY_BROKER_URL="redis://10.10.10.30:6379/0"
CELERY_RESULT_BACKEND="redis://10.10.10.30:6379/1"
```

然后只启动应用与 worker（不启动本地 mysql/redis 容器）：

```bash
docker compose up --build api worker
```

#### 场景 B：使用本地容器版 MySQL/Redis

使用 `local-infra` profile 启动完整栈：

```bash
docker compose --profile local-infra up --build
```

此时建议 `.env` 使用默认：`MYSQL_HOST="mysql"`，`CELERY_*` 里的 Redis 主机为 `redis`。

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

- `MYSQL_HOST` 改成 `127.0.0.1` 或实际地址
- `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` 改成实际 Redis 地址

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
