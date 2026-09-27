from typing import List
from fastapi import APIRouter, Depends
from dependencies import get_monitor
from domain.schemas import GetTopProcessSchema
from domain.services import ProcessService
from monitor import MonitorTask

process_router = APIRouter()


@process_router.get(
    "/usageProcess",
    response_model=List[GetTopProcessSchema],
)
async def get_process(
    monitor: MonitorTask = Depends(get_monitor),
    service: ProcessService = Depends(ProcessService),
) -> List[GetTopProcessSchema]:
    """
    Route to get biggest Process.

    Args:
        monitor (MonitorTask): Injected monitoring task.
        service (ProcessService): Injected process service.

    Returns:
        List[GetTopProcessSchema]: A list of Process as per the response model.
    """
    return await service.get_process(monitor)
