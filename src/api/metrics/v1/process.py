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
    Route to get biggest Process.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetTopProcessSchema]: A list of Process as per the response model.
    """
    return await ProcessService().get_process(request.app.state.monitortask)