from typing import List
from fastapi import APIRouter, Depends
from dependencies import get_monitor
from domain.schemas import GetNetworkResponseSchema
from domain.services import NetworkService
from monitor import MonitorTask

network_router = APIRouter()


@network_router.get(
    "/usageNetwork",
    response_model=List[GetNetworkResponseSchema],
)
async def get_network(
    monitor: MonitorTask = Depends(get_monitor),
    service: NetworkService = Depends(NetworkService),
) -> List[GetNetworkResponseSchema]:
    """
    Route to get the network counters of each interface.

    Args:
        monitor (MonitorTask): Injected monitoring task.
        service (NetworkService): Injected network service.

    Returns:
        List[GetNetworkResponseSchema]: One entry per network interface.
    """
    return await service.get_network_statut(monitor)
