from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from datetime import datetime
import model
from database import get_db
from auth import hash_password

router = APIRouter(prefix="/users",tags=["Users"])

class UserCreate(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    username : str
    created_at : datetime

@router.post("/register", status_code= 201, response_model= UserResponse)
def register(user: UserCreate, db:Session = Depends(get_db)):
    existing = db.query(model.User).filter(model.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="already taken")
    db_user = model.User(username=user.username, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


