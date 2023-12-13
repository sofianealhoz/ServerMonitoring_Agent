from fastapi import APIRouter, Request
from domain.schemas import GetSystemInfoResponseSchema, ExceptionResponseSchema
from domain.services import SystemService

system_router = APIRouter()

@system_router.get(
    "/system-info",
    response_model=GetSystemInfoResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_system_info_route(request: Request) -> GetSystemInfoResponseSchema:
    """
    Route to get system information.

    Args:
        request (Request): The incoming request.

    Returns:
        GetSystemInfoResponseSchema: System information as per the response model.
    """
    system_info = SystemService().get_system_info()
    return GetSystemInfoResponseSchema(nickname=system_info.nickname, hostname=system_info.hostname, ip_address=system_info.ip_address)
