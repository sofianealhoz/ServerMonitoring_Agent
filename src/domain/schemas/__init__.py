from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema
from .hdd import GetHddUsageResponseSchema
from .ram import GetRamResponseSchema
from .log import GetLogResponseSchema
from .network import GetNetworkResponseSchema
from .process import GetTopProcessSchema
from .user import GetUserResponseSchema
from .metrics import MetricSampleCreateSchema, MetricSampleSchema


class ExceptionResponseSchema(BaseModel):
    """Body of every error response, as built by the exception handlers in server.py."""

    error_code: int
    message: str


__all__ = [
    "GetCpuResponseSchema",
    "GetCpuCoreResponseSchema",
    "GetHddUsageResponseSchema",
    "GetRamResponseSchema",
    "GetNetworkResponseSchema",
    "ExceptionResponseSchema",
    "GetLogResponseSchema",
    "GetTopProcessSchema",
    "GetUserResponseSchema",
    "MetricSampleCreateSchema",
    "MetricSampleSchema",
]
