from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema
from .ram import GetRamResponseSchema


class ExceptionResponseSchema(BaseModel):
    error: str


__all__ = [
    "GetCpuResponseSchema",
    "GetCpuCoreResponseSchema",
    "ExceptionResponseSchema",
    "GetRamResponseSchema",
]
