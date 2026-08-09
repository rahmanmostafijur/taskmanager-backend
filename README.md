# Task Manager API

A REST API for managing tasks, built with FastAPI and PostgreSQL.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker & Docker Compose
- Python 3.12

## Getting Started

### With Docker

```bash
docker compose up
```

The API will be available at http://localhost:8000/docs

### With virtual environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /tasks/ | Get all tasks |
| POST | /tasks/ | Create a new task |
| GET | /tasks/{task_id} | Get a single task |
| PUT | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |

## Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://user:password@localhost:5432/taskmanager
```

When running with Docker Compose, this value is set automatically.