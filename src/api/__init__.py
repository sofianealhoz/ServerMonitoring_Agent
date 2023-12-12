from fastapi import APIRouter
from api.metrics.v1.cpu import cpu_router as cpu_v1_router
from api.metrics.v1.harddrive import hdd_router as hdd_v1_router
from api.metrics.v1.ram import ram_router as ram_v1_router
from api.metrics.v1.log import log_router as log_v1_router
from api.metrics.v1.network import network_router as network_v1_router
from api.metrics.v1.process import process_router as process_v1_router


router = APIRouter()
router.include_router(cpu_v1_router, prefix="/metrics/v1/cpu")
router.include_router(hdd_v1_router, prefix="/metrics/v1/harddrive")
router.include_router(ram_v1_router, prefix="/metrics/v1/ram")
router.include_router(log_v1_router, prefix="/metrics/v1/log")
router.include_router(network_v1_router, prefix="/metrics/v1/network")
router.include_router(process_v1_router, prefix="/metrics/v1/process")
__all__ = ["router"]
