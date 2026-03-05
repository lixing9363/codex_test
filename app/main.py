from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"message": "FastAPI + MySQL + Celery is running"}


app.include_router(api_router, prefix=settings.api_prefix)
