from fastapi import FastAPI
import model
from database import engine
from routers import items, tasks, users
from fastapi.middleware.cors import CORSMiddleware

# model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Task Manager API!"}