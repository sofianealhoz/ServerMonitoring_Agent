import asyncpg
from core.config import get_config

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
    await init_pool()
    assert _pool is not None
    async with _pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, cpu_usage, ram_usage, disk_usage FROM metric_samples ORDER BY id DESC LIMIT $1",
            limit,
        )
    return [dict(row) for row in rows]


