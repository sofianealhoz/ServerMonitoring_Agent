import asyncpg
from fastapi import APIRouter, Depends, Path, Query, Response, status
from core.exceptions import NotFoundException
from dependencies import get_db_connection
from domain.schemas import ExceptionResponseSchema
from domain.schemas.metrics import MetricSampleCreateSchema, MetricSampleSchema
from infrastructure.database import fetch_metric_sample, fetch_metric_samples, insert_metric_sample

history_router = APIRouter()


@history_router.get(
    "/history",
    response_model=list[MetricSampleSchema],
    responses={503: {"model": ExceptionResponseSchema}},
)
async def get_history(
    # Query parameter ?limit=..., validated: 422 if not an integer between 1 and 1000
    limit: int = Query(100, ge=1, le=1000, description="Number of samples to return"),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    rows = await fetch_metric_samples(conn, limit)
    return [MetricSampleSchema(**row) for row in rows]


@history_router.get(
    "/history/{sample_id}",
    response_model=MetricSampleSchema,
    responses={404: {"model": ExceptionResponseSchema}, 503: {"model": ExceptionResponseSchema}},
)
async def get_history_sample(
    # Path parameter /history/42, validated: 422 if not a positive integer
    sample_id: int = Path(ge=1, description="Id of the sample"),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    row = await fetch_metric_sample(conn, sample_id)
    if row is None:
        raise NotFoundException(f"Metric sample {sample_id} not found")
    return MetricSampleSchema(**row)


@history_router.post(
    "/history",
    response_model=MetricSampleSchema,
    status_code=status.HTTP_201_CREATED,
    responses={503: {"model": ExceptionResponseSchema}},
)
async def create_history_sample(
    # Request body: JSON parsed and validated against the schema, 422 if it does not match
    sample: MetricSampleCreateSchema,
    response: Response,
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    row = await insert_metric_sample(conn, sample.cpu_usage, sample.ram_usage, sample.disk_usage)
    # REST convention for a creation: 201 + the URL of the new resource
    response.headers["Location"] = f"/history/{row['id']}"
    return MetricSampleSchema(**row)
