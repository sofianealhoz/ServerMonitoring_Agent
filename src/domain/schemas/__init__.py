from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema
from .hdd import GetHddUsageResponseSchema
from .ram import GetRamResponseSchema
from .log import GetLogResponseSchema
from .network import GetNetworkResponseSchema
from .process import GetTopProcessSchema
from .user import GetUserResponseSchema
from .metrics import MetricSampleSchema


class ExceptionResponseSchema(BaseModel):
    error: str


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
    "MetricSampleSchema",
]
