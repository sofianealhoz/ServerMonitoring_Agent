"""
Dependencies injected into the routes with FastAPI's Depends().

A route declares what it needs in its signature; FastAPI calls these functions on each
request and passes the result. Tests replace them with app.dependency_overrides.
"""
from typing import AsyncIterator

import asyncpg
from fastapi import Request

from core.exceptions import ServiceUnavailableException
from infrastructure import database
from monitor import MonitorTask


def get_monitor(request: Request) -> MonitorTask:
    """The single MonitorTask created in create_app and fed by the monitoring thread."""
    return request.app.state.monitortask


async def get_db_connection() -> AsyncIterator[asyncpg.Connection]:
    """
    Borrow a connection from the pool for the duration of the request.

    The code after `yield` runs once the response is sent: the connection always goes back
    to the pool, even if the route raised an exception.

    Raises:
        ServiceUnavailableException: the pool cannot be created or no connection is available.
    """
    try:
        await database.init_pool()
        conn = await database.get_pool().acquire()
    except (OSError, asyncpg.PostgresError) as exc:
        raise ServiceUnavailableException("Database is unavailable") from exc
    try:
        yield conn
    finally:
        await database.get_pool().release(conn)
