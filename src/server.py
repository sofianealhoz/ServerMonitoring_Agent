"""
This module contains a FastAPI application with various routes and middleware.

It initializes the FastAPI app, sets up routers, event listeners, and exception handlers, and
creates a monitoring thread for fetching metrics.
"""
import threading
from typing import List
from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api import router
from api.default.default import default_router
from api.metrics.v1.cpu import cpu_router
from api.metrics.v1.harddrive import hdd_router
from api.metrics.v1.log import log_router
from api.metrics.v1.ram import ram_router
from api.metrics.v1.network import network_router
from api.metrics.v1.process import process_router
from api.metrics.v1.user import user_router
from core.exceptions import CustomException
from core.config import get_config
from monitor import MonitorTask


def init_routers(fastapi: FastAPI) -> None:
    """
    Initialize API routers and include them in the FastAPI fastapi.

    Args:
        fastapi (FastAPI): The FastAPI application to add routers to.
    """
    # Add default route (version, healthcheck)
    fastapi.include_router(default_router)
    # Add domain routes
    fastapi.include_router(router)
    fastapi.include_router(cpu_router)
    fastapi.include_router(hdd_router)
    fastapi.include_router(ram_router)
    fastapi.include_router(log_router)
    fastapi.include_router(network_router)
    fastapi.include_router(process_router)
    fastapi.include_router(user_router)


def init_listeners(fastapi: FastAPI) -> None:
    """
    Initialize event listeners and exception handlers for the FastAPI fastapi.

    Args:
        fastapi (FastAPI): The FastAPI application to set up event listeners and handlers for.
    """
    # Exception handler
    @fastapi.exception_handler(CustomException)
    async def custom_exception_handler(_request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

    # Start monitoring thread
    @fastapi.on_event("startup")
    def on_start_up():
        thread = threading.Thread(target=fastapi.state.monitortask.monitor, daemon=True)
        
        thread.start()


def make_middleware() -> List[Middleware]:
    """
    Create and return a list of middleware components, including CORS middleware.

    Returns:
        List[Middleware]: List of FastAPI middleware components.
    """
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    config = get_config()
    # Monitoring thread to fetch metrics
    monitortask = MonitorTask()
    # API
    fastapi = FastAPI(
        title=config.title,
        description=config.description,
        version=config.version,
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=make_middleware(),
    )
    fastapi.state.monitortask = monitortask
    fastapi.state.version = config.version
    init_routers(fastapi)
    init_listeners(fastapi)
    return fastapi


app = create_app()
