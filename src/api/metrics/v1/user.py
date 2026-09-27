from typing import List
from fastapi import APIRouter, Depends
from dependencies import get_monitor
from domain.schemas import GetUserResponseSchema
from domain.services.userservice import UserService
from monitor import MonitorTask

user_router = APIRouter()


@user_router.get(
    "/users",
    response_model=List[GetUserResponseSchema],
)
async def get_user(
    monitor: MonitorTask = Depends(get_monitor),
    service: UserService = Depends(UserService),
):
    """
    Route to get user info.

    Uses the application's MonitorTask (injected) instead of a private instance created at
    import time, whose monitoring thread was never started.

    Returns:
        List[GetUserResponseSchema]: A list of users and their info.
    """
    return await service.get_user(monitor)
