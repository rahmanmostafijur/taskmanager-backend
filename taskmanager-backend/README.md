# Task Manager API

A multi-user task management REST API built with FastAPI and PostgreSQL. Users register, log in, and manage their own tasks — each user can only see and modify tasks they own.

**Live demo:** https://taskmanager-backend-tclq.onrender.com/docs

> Hosted on Render's free tier, which spins down after inactivity. The first request may take up to 50 seconds while the instance wakes up.

---

## Tech Stack

- **FastAPI** — web framework, automatic OpenAPI docs
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Pydantic v2** — request validation and response serialization
- **pyJWT** — JWT creation and verification
- **bcrypt** — password hashing
- **Docker & Docker Compose** — containerization
- **GitHub Actions** — CI
- **pytest** — API tests via FastAPI's TestClient

---

## Features

**Authentication**
- Passwords hashed with bcrypt (salted, cost factor 12) — plaintext passwords are never stored
- JWT access tokens signed with HS256, 30-minute expiry
- OAuth2 password flow, compatible with the Swagger UI "Authorize" button
- Login failures return an identical message whether the username or the password was wrong, to avoid user enumeration

**Authorization**
- Every task is tied to its owner through a `user_id` foreign key
- All task endpoints require a valid token and filter by owner
- Requesting another user's task returns `404`, not `403` — the API does not reveal which task IDs exist

**Data layer**
- Alembic migrations run automatically on container startup, so schema changes deploy without data loss
- Response models act as a whitelist: `hashed_password` and `user_id` are never serialized into a response

**Infrastructure**
- Docker Compose with a PostgreSQL healthcheck, so the API waits until the database is ready to accept connections
- All secrets read from environment variables; nothing sensitive is committed

---

## Running Locally

**Prerequisites:** Docker and Docker Compose.

```bash
git clone https://github.com/rahmanmostafijur/taskmanager-backend.git
cd taskmanager-backend/taskmanager-backend
cp .env.example .env
```

Fill in `.env`:

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/taskmanager
POSTGRES_PASSWORD=yourpassword
SECRET_KEY=<generate one, see below>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Start the stack:

```bash
docker compose up --build
```

The API will be at http://localhost:8000 and the interactive docs at http://localhost:8000/docs.

Migrations run automatically when the container starts, so the schema is created on first launch.

---

## API Reference

### Users

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/users/register` | — | Create an account. JSON body. |
| `POST` | `/users/login` | — | Exchange credentials for a JWT. Form-encoded body (OAuth2 standard). |
| `GET` | `/users/me` | Bearer | Return the authenticated user. |

**Constraints:** username 6–50 characters, password 8–32 characters.

### Tasks

All task endpoints require an `Authorization: Bearer <token>` header and operate only on the authenticated user's tasks.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/tasks/` | List the current user's tasks. |
| `POST` | `/tasks/` | Create a task. |
| `GET` | `/tasks/{task_id}` | Fetch one task. |
| `PUT` | `/tasks/{task_id}` | Update a task. |
| `DELETE` | `/tasks/{task_id}` | Delete a task. |

### Items

`/items/` endpoints remain from an earlier stage of the project and are unauthenticated. They are not part of the task management feature set.

---

## Tests

    cd taskmanager-backend
    pytest

Three tests cover the authentication boundary: the root endpoint responds,
`/tasks/` rejects unauthenticated requests with `401`, and a malformed token
is rejected rather than causing a server error. They run on every push via
GitHub Actions before the Docker image is built.

## Example

Register:

```bash
curl -X POST https://taskmanager-backend-tclq.onrender.com/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "yourname", "password": "yourpassword"}'
```

Log in (note the form encoding):

```bash
curl -X POST https://taskmanager-backend-tclq.onrender.com/users/login \
  -d "username=yourname&password=yourpassword"
```

Create a task with the returned token:

```bash
curl -X POST https://taskmanager-backend-tclq.onrender.com/tasks/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Write documentation", "description": "Finish the README"}'
```

---

## Database Migrations

The project uses Alembic rather than `create_all()`, so schema changes can be applied to an existing database without dropping tables.

After changing a model in `model.py`:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

Inspect the generated file in `alembic/versions/` before applying it — autogenerate is a helpful starting point, not a guarantee.

---

## Project Structure

```
├── alembic/              # migration environment and versions
├── routers/
│   ├── users.py          # register, login, me
│   ├── tasks.py          # task CRUD, ownership-scoped
│   └── items.py
├── auth.py               # hashing, JWT, get_current_user dependency
├── database.py           # engine, session, Base
├── model.py              # SQLAlchemy models
├── main.py               # app entrypoint, router registration
├── start.sh              # runs migrations, then the server
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## Notes

This is a learning project built to practise backend fundamentals end to end: ORM modelling, authentication, containerization, migrations, and deployment. It is deployed on Render rather than AWS, but the deployment concepts — image builds, injected configuration, managed Postgres, migrations on startup — carry over directly.