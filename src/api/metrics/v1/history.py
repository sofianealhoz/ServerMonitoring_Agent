from fastapi import APIRouter, Query
from domain.schemas import ExceptionResponseSchema
from domain.schemas.metrics import MetricSampleSchema
from infrastructure.database import fetch_metric_samples

history_router = APIRouter()

@history_router.get(
    "/history",
    response_model=list[MetricSampleSchema],
    responses={503: {"model": ExceptionResponseSchema}},
)
async def get_history(limit: int = Query(100, ge=1, le=1000)):
    rows = await fetch_metric_samples(limit)
    return [MetricSampleSchema(**row) for row in rows]
