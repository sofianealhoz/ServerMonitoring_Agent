"""
This module defines API routes for handling RAM-related data.
"""
from typing import List
from fastapi import APIRouter, Depends
from dependencies import get_monitor
from domain.schemas import GetRamResponseSchema
from domain.services import RamService
from monitor import MonitorTask

ram_router = APIRouter()


@ram_router.get(
    "/usageRam",
    response_model=List[GetRamResponseSchema],
)
async def get_ram(
    monitor: MonitorTask = Depends(get_monitor),
    service: RamService = Depends(RamService),
) -> List[GetRamResponseSchema]:
    """
    Route to get a list of RAM data.

    Args:
        monitor (MonitorTask): Injected monitoring task.
        service (RamService): Injected RAM service.

    Returns:
        List[GetRamResponseSchema]: A list of RAM data as per the response model.
    """
    return await service.get_ram(monitor)
