from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from datetime import datetime
import model
from database import get_db
from auth import hash_password, verify_password, create_access_token, get_current_user

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
        raise HTTPException(status_code=400, detail="username already taken")
    db_user = model.User(username=user.username, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(model.User).filter(model.User.username == from_data.username).first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(from_data.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": existing_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: model.User = Depends(get_current_user)):
    return current_user




