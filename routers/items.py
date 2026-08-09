from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import model
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/items", tags=["Items"])

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_offer: bool | None = None

@router.post("/")
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = model.Item(name=item.name, description=item.description, price=item.price, is_offer=item.is_offer)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item created successfully", "item": db_item}

@router.get("/")
def get_all_items(db: Session = Depends(get_db)):
    items = db.query(model.Item).all()
    return items

@router.get("/{item_id}")
def get_one_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(model.Item).filter(model.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}")
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = db.query(model.Item).filter(model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(model.Item).filter(model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully", "item": db_item}