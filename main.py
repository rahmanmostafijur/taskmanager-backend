from fastapi import FastAPI
import model
from database import engine
from routers import items, tasks

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Task Manager API!"}