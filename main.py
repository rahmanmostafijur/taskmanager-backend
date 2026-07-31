from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import model
from database import engine, get_db
from sqlalchemy.orm import Session


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_offer: bool | None = None

items = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items/")
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = model.Item(name=item.name, description=item.description, price=item.price, is_offer=item.is_offer)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item created successfully", "item": db_item}

@app.get("/items/")
def get_all_items(db: Session = Depends(get_db)):
    items = db.query(model.Item).all()
    return items

@app.get("/items/{item_id}")
def get_one_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(model.Item).filter(model.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = db.query(model.Item).filter(model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(model.Item).filter(model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully", "item": db_item}
