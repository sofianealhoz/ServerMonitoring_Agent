"""
This module defines API routes for handling log-related data.
"""
from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetLogResponseSchema,
)
from domain.services import LogService

log_router = APIRouter()


@log_router.get(
    "/logMessage",
    response_model=List[GetLogResponseSchema],
    # response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_log(request: Request) -> List[GetLogResponseSchema]:
    """
    Route to get a list of Log data.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetLogResponseSchema]: A list of Log data as per the response model.
    """
    return await LogService().get_log(request.app.state.monitortask)
