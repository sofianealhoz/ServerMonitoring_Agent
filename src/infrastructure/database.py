import logging
from decimal import Decimal

import asyncpg
from core.config import get_config
from core.exceptions import ServiceUnavailableException

logger = logging.getLogger(__name__)

_pool: asyncpg.Pool | None = None

async def init_pool() -> None:
    global _pool
    if _pool is None:
        cfg=get_config()
        _pool = await asyncpg.create_pool(
            dsn=cfg.database_url,
            min_size=cfg.database_pool_size,
            max_size=cfg.database_pool_size + cfg.database_max_overflow,
        )

def get_pool() -> asyncpg.Pool:
    assert _pool is not None, "init_pool() must run first"
    return _pool

async def close_pool() -> None:
    if _pool:
        await _pool.close()

async def fetch_metric_samples(conn: asyncpg.Connection, limit: int = 100) -> list[dict]:
    """
    Read the most recent metric samples with the connection injected by the route.

    Raises:
        ServiceUnavailableException: the query failed (missing table, lost connection...).
    """
    try:
        rows = await conn.fetch(
            "SELECT id, cpu_usage, ram_usage, disk_usage FROM metric_samples ORDER BY id DESC LIMIT $1",
            limit,
        )
    except (OSError, asyncpg.PostgresError) as exc:
        # Translate the technical error into a domain error; keep the cause for the logs
        logger.error("Metric history query failed: %s", exc)
        raise ServiceUnavailableException("Metrics history is unavailable") from exc
    return [dict(row) for row in rows]

async def fetch_metric_sample(conn: asyncpg.Connection, sample_id: int) -> dict | None:
    """Read one metric sample by id; None when it does not exist."""
    try:
        row = await conn.fetchrow(
            "SELECT id, cpu_usage, ram_usage, disk_usage FROM metric_samples WHERE id = $1",
            sample_id,
        )
    except (OSError, asyncpg.PostgresError) as exc:
        logger.error("Metric sample query failed: %s", exc)
        raise ServiceUnavailableException("Metrics history is unavailable") from exc
    return dict(row) if row else None

async def fetch_user(conn: asyncpg.Connection, username: str) -> dict | None:
    """Read one API account by username; None when it does not exist."""
    try:
        row = await conn.fetchrow(
            "SELECT username, hashed_password, role, disabled FROM users WHERE username = $1",
            username,
        )
    except (OSError, asyncpg.PostgresError) as exc:
        logger.error("User query failed: %s", exc)
        raise ServiceUnavailableException("Authentication is unavailable") from exc
    return dict(row) if row else None

async def insert_metric_sample(
    conn: asyncpg.Connection, cpu_usage: Decimal, ram_usage: Decimal, disk_usage: Decimal
) -> dict:
    """Insert one metric sample and return the stored row, id included."""
    try:
        row = await conn.fetchrow(
            "INSERT INTO metric_samples (cpu_usage, ram_usage, disk_usage) VALUES ($1, $2, $3)"
            " RETURNING id, cpu_usage, ram_usage, disk_usage",
            cpu_usage, ram_usage, disk_usage,
        )
    except (OSError, asyncpg.PostgresError) as exc:
        logger.error("Metric sample insert failed: %s", exc)
        raise ServiceUnavailableException("Metrics history is unavailable") from exc
    return dict(row)
