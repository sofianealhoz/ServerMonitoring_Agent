from fastapi import APIRouter
from api.metrics.v1.cpu import cpu_router as cpu_v1_router
from api.metrics.v1.harddrive import hdd_router as hdd_v1_router
from api.metrics.v1.ram import ram_router as ram_v1_router
from api.metrics.v1.network import network_router as network_v1_router


router = APIRouter()
router.include_router(cpu_v1_router, prefix="/metrics/v1/cpu")
router.include_router(hdd_v1_router, prefix="/metrics/v1/harddrive")
router.include_router(ram_v1_router, prefix="/metrics/v1/ram")
router.include_router(network_v1_router, prefix="/metrics/v1/network")
__all__ = ["router"]
