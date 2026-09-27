"""
This module defines API routes for handling log-related data.
"""
from typing import List
from fastapi import APIRouter, Depends
from dependencies import get_monitor
from domain.schemas import GetLogResponseSchema
from domain.services import LogService
from monitor import MonitorTask

log_router = APIRouter()


@log_router.get(
    "/logMessage",
    response_model=List[GetLogResponseSchema],
    # response_model_exclude={"id"},
)
async def get_log(
    monitor: MonitorTask = Depends(get_monitor),
    service: LogService = Depends(LogService),
) -> List[GetLogResponseSchema]:
    """
    Route to get a list of Log data.

    Args:
        monitor (MonitorTask): Injected monitoring task.
        service (LogService): Injected log service.

    Returns:
        List[GetLogResponseSchema]: A list of Log data as per the response model.
    """
    return await service.get_log(monitor)
