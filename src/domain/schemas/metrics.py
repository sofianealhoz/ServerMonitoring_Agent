from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MetricSampleCreateSchema(BaseModel):
    """
    Request body of POST /history: what the client sends to record one sample.

    No `id`: the database generates it. Percentages must be between 0 and 100, and unknown
    fields are rejected. Any mismatch makes FastAPI answer 422 before the route runs.
    """

    model_config = ConfigDict(extra="forbid")

    cpu_usage: Decimal = Field(ge=0, le=100, description="CPU usage, in percent")
    ram_usage: Decimal = Field(ge=0, le=100, description="RAM usage, in percent")
    disk_usage: Decimal = Field(ge=0, le=100, description="Disk usage, in percent")


class MetricSampleSchema(BaseModel):
    """Response body: one stored sample, with the id given by the database."""

    id: int
    cpu_usage: Decimal | None = None
    ram_usage: Decimal | None = None
    disk_usage: Decimal | None = None
