# Task Manager

A multi-user task management application. Users register, log in, and manage
their own tasks — each user can only see and modify tasks they own.

**Live API:** https://taskmanager-backend-tclq.onrender.com/docs

> Hosted on Render's free tier, which spins down after inactivity.
> The first request may take up to 50 seconds while the instance wakes up.

## Repository Layout

| Folder | Contents |
|---|---|
| [`taskmanager-backend/`](./taskmanager-backend) | FastAPI + PostgreSQL REST API. JWT auth, Alembic migrations, Docker, pytest. **Start here** — full setup instructions and API reference. |
| `taskmanager-frontend/` | Browser client. In progress. |

## Status

The backend is complete and deployed. The frontend is an in-progress
plain HTML/JavaScript client built to understand `fetch`, tokens, and
DOM manipulation before moving to React.