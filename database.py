from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = "postgresql://postgres:16189251@localhost:5432/taskmanager"

engine = create_engine(database_url)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
