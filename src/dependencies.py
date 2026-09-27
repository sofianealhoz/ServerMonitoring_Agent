"""
Dependencies injected into the routes with FastAPI's Depends().

A route declares what it needs in its signature; FastAPI calls these functions on each
request and passes the result. Tests replace them with app.dependency_overrides.
"""
from typing import AsyncIterator

import asyncpg
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from core.exceptions import ForbiddenException, ServiceUnavailableException, UnauthorizedException
from core.security import decode_access_token
from domain.schemas.auth import CurrentUserSchema
from infrastructure import database
from monitor import MonitorTask

# Reads the "Authorization: Bearer <token>" header. tokenUrl tells /docs where to log in.
# auto_error=False: we raise our own 401, in the same JSON format as the other errors.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_monitor(request: Request) -> MonitorTask:
    """The single MonitorTask created in create_app and fed by the monitoring thread."""
    return request.app.state.monitortask


async def get_db_connection() -> AsyncIterator[asyncpg.Connection]:
    """
    Borrow a connection from the pool for the duration of the request.

    The code after `yield` runs once the route has finished: the connection always goes back
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


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    conn: asyncpg.Connection = Depends(get_db_connection),
) -> CurrentUserSchema:
    """
    Authenticate the request: who is calling?

    Raises:
        UnauthorizedException (401): no token, bad signature, expired, or unknown user.
        ForbiddenException (403): the account exists but is disabled.
    """
    if token is None:
        raise UnauthorizedException("Not authenticated")
    username = decode_access_token(token)
    # Read the account on every request: a disabled user or a changed role applies at once
    user = await database.fetch_user(conn, username)
    if user is None:
        raise UnauthorizedException("Invalid token")
    if user["disabled"]:
        raise ForbiddenException("Account disabled")
    return CurrentUserSchema(username=user["username"], role=user["role"])


def require_admin(user: CurrentUserSchema = Depends(get_current_user)) -> CurrentUserSchema:
    """
    Authorize the request: is this caller allowed to do this?

    Raises:
        ForbiddenException (403): authenticated, but not an admin.
    """
    if user.role != "admin":
        raise ForbiddenException("Admin role required")
    return user
