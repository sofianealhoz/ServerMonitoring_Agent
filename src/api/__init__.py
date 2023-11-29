from fastapi import APIRouter
from api.metrics.v1.cpu import cpu_router as cpu_v1_router
from api.metrics.v1.harddrive import hdd_router as hdd_v1_router

router = APIRouter()
router.include_router(cpu_v1_router, prefix="/metrics/v1/cpu")
router.include_router(hdd_v1_router, prefix="/metrics/v1/harddrive")

__all__ = ["router"]
