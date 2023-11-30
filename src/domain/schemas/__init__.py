from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema
from .hdd import GetHddUsageResponseSchema
from .ram import GetRamResponseSchema



class ExceptionResponseSchema(BaseModel):
    error: str


__all__ = [
    "GetCpuResponseSchema",
    "GetCpuCoreResponseSchema",
    "GetHddUsageResponseSchema",
    "GetRamResponseSchema",
    "ExceptionResponseSchema",
]
