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

## Install and run

With the Makefile:

    make environment
    make run

With Docker:

    docker build -t monitoring-agent .
    docker run -d -p 8000:8000 monitoring-agent

## Note

Team project (Telecom Saint-Etienne). The agent collects the metrics; the
companion web interface consumes its API.
