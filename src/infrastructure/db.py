from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import get_config
from contextlib import asynccontextmanager


cfg = get_config()
async_engine = create_async_engine(
    cfg.database_url,
    echo=True,
    pool_size=cfg.database_pool_size,
    max_overflow=cfg.database_max_overflow,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=False,
)

@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session