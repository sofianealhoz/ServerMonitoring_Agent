from fastapi import APIRouter, Depends
from dependencies import get_monitor
from domain.schemas import (
    ExceptionResponseSchema,
    GetHddUsageResponseSchema,
)
from domain.services import HardDriveService
from monitor import MonitorTask

hdd_router = APIRouter()


@hdd_router.get(
    "/usageHdd",
    response_model=GetHddUsageResponseSchema,
    # response_model_exclude={"id"},
    responses={503: {"model": ExceptionResponseSchema}},
)
async def get_hdd(
    monitor: MonitorTask = Depends(get_monitor),
    service: HardDriveService = Depends(HardDriveService),
) -> GetHddUsageResponseSchema:
    """
    Route to get the disk usage.

    Args:
        monitor (MonitorTask): Injected monitoring task.
        service (HardDriveService): Injected disk service.

    Returns:
        GetHddUsageResponseSchema: Disk usage as per the response model.
    """
    return await service.get_harddrive_usage(monitor)
