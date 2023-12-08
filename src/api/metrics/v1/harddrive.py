from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetHddUsageResponseSchema,
)

from domain.services import HardDriveService

hdd_router = APIRouter()


@hdd_router.get(
    "/usageHdd",
    response_model=GetHddUsageResponseSchema,
    # response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_hdd(request: Request) -> GetHddUsageResponseSchema:
    """
    Route to get a list of CPU data.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetCpuResponseSchema]: A list of CPU data as per the response model.
    """
    return await HardDriveService().get_harddrive_usage(request.app.state.monitortask)
