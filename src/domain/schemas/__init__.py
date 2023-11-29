from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema
from .hdd import GetHddResponseSchema#, GetHddPartResponseSchema


class ExceptionResponseSchema(BaseModel):
    error: str


__all__ = [
    "GetCpuResponseSchema",
    "GetCpuCoreResponseSchema",
    "GetHddResponseSchema",
    #"GetHddPartResponseSchema",
    "ExceptionResponseSchema",
]
