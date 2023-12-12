from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetTopProcessSchema,
)

from domain.services import ProcessService

process_router = APIRouter()


@process_router.get(
    "/usageProcess",
    response_model=List[GetTopProcessSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_ram(request: Request) -> List[GetTopProcessSchema]:
    """
    Route to get a list of RAM data.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetRamResponseSchema]: A list of RAM data as per the response model.
    """
    return await ProcessService().get_process(request.app.state.monitortask)