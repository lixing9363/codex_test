from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemRead)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.id == payload.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    item = Item(title=payload.title, owner_id=payload.owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
