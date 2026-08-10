from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import model
from pydantic import BaseModel, ConfigDict
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    is_done: bool  | None = False

class TaskResponseCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str |  None
    is_done: bool | None = False
    created_at: datetime

@router.post("/", status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_user)):
    db_task = model.Task(title=task.title, description=task.description, is_done=task.is_done, user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return {"message": "Task created successfully", "task": db_task}

@router.get("/", response_model=list[TaskResponseCreate])
def get_all_tasks(db: Session = Depends(get_db), current_user: model.User = Depends(get_current_user)):
    tasks = db.query(model.Task).filter(model.Task.user_id == current_user.id).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponseCreate)
def get_one_task(task_id: int, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_user)):
    task = db.query(model.Task).filter(model.Task.id == task_id, model.Task.user_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponseCreate)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_user)):
    db_task = db.query(model.Task).filter(model.Task.id == task_id, model.Task.user_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="task not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", response_model=TaskResponseCreate)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_user)):
    db_task = db.query(model.Task).filter(model.Task.id == task_id, model.Task.user_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="task not found")
    db.delete(db_task)
    db.commit()
    return db_task

