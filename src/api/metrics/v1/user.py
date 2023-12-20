from typing import List
from fastapi import APIRouter, Request
from monitor import MonitorTask
from domain.schemas import (
    ExceptionResponseSchema, 
    GetUserResponseSchema,
)
from domain.services.userservice import UserService

user_router = APIRouter()
user_service = UserService()
monitor_task = MonitorTask()

@user_router.get(
    "/users",
    response_model=List[GetUserResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_user():
    """
    Route to get user info.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetUserResponseSchema]: A list of users and their info.
    """

    users = await user_service.get_user(monitor_task)
    return users  # Retournez simplement les utilisateurs, sans les imprimer