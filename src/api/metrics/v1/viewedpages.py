from fastapi import APIRouter
from monitor import MonitorTask
from domain.schemas import (
    ExceptionResponseSchema
)
from domain.schemas.viewedpages import GetViewedPagesResponseSchema
from domain.services.viewedpagesservice import ViewedPagesService

viewedpages_router = APIRouter()
viewedpages_service = ViewedPagesService()
monitor_task = MonitorTask()

@viewedpages_router.get(
    "/most-viewed-pages",
    response_model=GetViewedPagesResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_most_viewed_page():
    """
    Route to get most viewed page's info.

    Args:
        request (Request): The incoming request.

    Returns:
        GetViewedPagesResponseSchema: The most viewed page's info.
    """

    viewedpages = await viewedpages_service.get_most_viewed_page(monitor_task)
    return viewedpages