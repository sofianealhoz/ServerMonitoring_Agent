# Server Monitoring Agent

Agent that exposes a machine's system metrics over an HTTP API: CPU, RAM,
disk and network. It is meant to be queried by the monitoring interface
(see Server Monitoring Interface).

## Stack

- Python 3
- FastAPI + Uvicorn (API)
- PostgreSQL + SQLAlchemy (storage)
- Docker, GitLab CI, pytest
- Makefile for common tasks

## Structure

- `src/api` : API routes.
- `src/core` : application logic.
- `src/domain` : domain models.
- `src/infrastructure` : access to system resources.
- `src/monitor` : metric collection.
- `src/main.py`, `src/server.py` : entry points.
- `src/tests` : tests.

## Configuration

Environment variables:

- `AGENT_ENV` : `local` or `production`.
- `AGENT_VERSION` : version exposed on `/version`.
- `AGENT_DESCRIPTION` : application description.
- `AGENT_DEBUG` : enable debug mode.
- `AGENT_DATABASE_URL` : PostgreSQL connection string (required).
- `AGENT_JWT_SECRET` : key used to sign access tokens (required).

Secrets are read from the environment only. Copy `.env.example` to `.env` (ignored by git).

## Database

    psql "$AGENT_DATABASE_URL" -f sql/schema.sql
    python3 src/create_user.py alice admin      # prompts for the password

## Authentication

Every metrics route requires a JWT; `/`, `/health`, `/version` and `/token` are public.

    # 1. get a token (OAuth2 password flow, form-encoded)
    curl -X POST http://localhost:8000/token -d "username=alice&password=..."
    # 2. send it on each call
    curl http://localhost:8000/usage -H "Authorization: Bearer <access_token>"

- `401 Unauthorized` : missing, invalid or expired token.
- `403 Forbidden` : valid token, but the role is not allowed (writing to `/history` needs `admin`).

## Install and run

With the Makefile:

    make environment
    make run

With Docker:

    docker build -t monitoring-agent .
    docker run -d -p 8000:8000 --env-file .env monitoring-agent

## Note

Team project (Telecom Saint-Etienne). The agent collects the metrics; the
companion web interface consumes its API.
