import logging

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

async def close_pool() -> None:
    if _pool:
        await _pool.close()

async def fetch_metric_samples(limit: int = 100) -> list[dict]:
    """
    Read the most recent metric samples.

    Raises:
        ServiceUnavailableException: PostgreSQL is unreachable or the query failed.
    """
    try:
        await init_pool()
        assert _pool is not None
        async with _pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, cpu_usage, ram_usage, disk_usage FROM metric_samples ORDER BY id DESC LIMIT $1",
                limit,
            )
    except (OSError, asyncpg.PostgresError) as exc:
        # Translate the technical error into a domain error; keep the cause for the logs
        logger.error("Metric history query failed: %s", exc)
        raise ServiceUnavailableException("Metrics history is unavailable") from exc
    return [dict(row) for row in rows]
