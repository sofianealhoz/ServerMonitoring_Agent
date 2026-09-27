"""
This module defines API routes for handling CPU-related data.
"""
from typing import List
from fastapi import APIRouter, Depends
from dependencies import get_monitor
from domain.schemas import (
    ExceptionResponseSchema,
    GetCpuResponseSchema,
    GetCpuCoreResponseSchema,
)
from domain.services import CpuService
from monitor import MonitorTask

cpu_router = APIRouter()


@cpu_router.get(
    "/usage",
    response_model=List[GetCpuResponseSchema],
    # response_model_exclude={"id"},
    responses={503: {"model": ExceptionResponseSchema}},
)
async def get_cpu(
    monitor: MonitorTask = Depends(get_monitor),
    service: CpuService = Depends(CpuService),
) -> List[GetCpuResponseSchema]:
    """
    Route to get a list of CPU data.

    Args:
        monitor (MonitorTask): Injected monitoring task.
        service (CpuService): Injected CPU service.

    Returns:
        List[GetCpuResponseSchema]: A list of CPU data as per
        the response model.
    """
    return await service.get_cpu(monitor)


@cpu_router.get(
    "/core",
    response_model=GetCpuCoreResponseSchema,
    # response_model_exclude={"id"},
)
async def get_core_number(monitor: MonitorTask = Depends(get_monitor)) -> GetCpuCoreResponseSchema:
    """
    Route to get the number of CPU core.

    Args:
        monitor (MonitorTask): Injected monitoring task.

    Returns:
        int: number of cpu core.
    """
    return GetCpuCoreResponseSchema(number=monitor.num_cores)
