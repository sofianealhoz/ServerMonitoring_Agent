from fastapi import APIRouter, Query
from domain.schemas.metrics import MetricSampleSchema
#from infrastructure.database import fetch_metric_samples
from infrastructure.repositories.metrics import fetch_metric_samples

history_router = APIRouter()

@history_router.get("/history", response_model = list[MetricSampleSchema])
async def get_history(limit: int = 100):
    rows = await fetch_metric_samples()
    return [MetricSampleSchema(**row) for row in rows]