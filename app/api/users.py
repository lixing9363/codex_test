from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.tasks.jobs import send_welcome_email

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(name=payload.name, email=payload.email)
    db.add(user)
    db.commit()
    db.refresh(user)

    send_welcome_email.delay(user.email)
    return user


@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
