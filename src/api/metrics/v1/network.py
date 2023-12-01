from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetNetworkResponseSchema,
)

from domain.services import NetworkService

network_router = APIRouter()

@network_router.get(
    "/usageNetwork",
    response_model=List[GetNetworkResponseSchema],
    # response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_network(request: Request) -> List[GetNetworkResponseSchema]:
    """
    Route to get a list of CPU data.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetCpuResponseSchema]: A list of CPU data as per the response model.
    """
    #return Response(content='{"message": "Hello World"}', status_code=200)
    return await NetworkService().get_network_statut(request.app.state.monitortask)
