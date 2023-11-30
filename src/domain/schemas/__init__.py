from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema
from .hdd import GetHddUsageResponseSchema


class ExceptionResponseSchema(BaseModel):
    error: str


__all__ = [
    "GetCpuResponseSchema",
    "GetCpuCoreResponseSchema",
    "GetHddUsageResponseSchema",
    #"GetHddPartResponseSchema",
    "ExceptionResponseSchema",
]
