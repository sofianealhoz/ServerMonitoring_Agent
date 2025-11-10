from sqlalchemy import text
from infrastructure.db import get_session
from domain.schemas.metrics import MetricSampleSchema

SQL_FETCH_METRICS = text("""
    SELECT cpu_usage, ram_usage, disk_usage
    FROM metric_samples                         
""")

async def fetch_metric_samples():
    async with get_session() as session:
        result = await session.execute(SQL_FETCH_METRICS)
        return [dict(row._mapping) for row in result]
    
SQL_INSERT_METRIC = text("""
    INSERT INTO metric_samples (cpu_usage, ram_usage, disk_usage)
    VALUES (:cpu_usage, :ram_usage, :disk_usage)
""")

async def insert_metric_sample(sample: MetricSampleSchema) -> None:
    async with get_session() as session:
        await session.execute(SQL_INSERT_METRIC, sample.model_dump())
        await session.commit()