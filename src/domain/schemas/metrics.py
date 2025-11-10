from pydantic import BaseModel
from decimal import Decimal

class MetricSampleSchema(BaseModel):
    cpu_usage: Decimal | None = None
    ram_usage: Decimal | None = None
    disk_usage: Decimal | None = None