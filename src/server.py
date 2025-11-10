"""
This module contains a FastAPI application with various routes and middleware.

It initializes the FastAPI app, sets up routers, event listeners, and exception handlers, and
creates a monitoring thread for fetching metrics.
"""
import threading
import asyncio
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
from api.metrics.v1.history import history_router
from core.exceptions import CustomException
from core.config import get_config
from monitor import MonitorTask
#from infrastructure.database import init_pool, close_pool
# from sqlalchemy import select
# from infrastructure.db import get_session, metric_samples
from infrastructure.db import async_engine
from infrastructure.repositories.metrics import insert_metric_sample 

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
    fastapi.include_router(history_router)


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
    async def on_start_up():
        #await init_pool()
        loop = asyncio.get_running_loop()
        metric_queue = asyncio.Queue(maxsize=1000)
        fastapi.state.metric_queue = metric_queue
        fastapi.state.metric_writer = asyncio.create_task(worker(metric_queue, insert_metric_sample))
    # Monitoring thread to fetch metrics
    
        monitortask = MonitorTask(
            publish_metric=make_sink(loop, metric_queue),
            # publish_network=make_sink(loop, network_queue),
            # publish_process=make_sink(loop, process_queue),
            # publish_logs=make_sink(loop, log_queue),
            # publish_user=make_sink(loop, user_queue),
        )    # API
        fastapi.state.monitortask = monitortask
        thread = threading.Thread(target=fastapi.state.monitortask.monitor, daemon=True)


        thread.start()
    
    @fastapi.on_event("shutdown")
    async def on_shutdown():
        await async_engine.dispose()

        #await close_pool()



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
    fastapi = FastAPI(
        title=config.title,
        description=config.description,
        version=config.version,
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=make_middleware(),
    )
    fastapi.state.monitortask = None
    fastapi.state.version = config.version
    fastapi.state.metric_queue = None
    fastapi.state.metric_writer = None
    init_routers(fastapi)
    init_listeners(fastapi)
    return fastapi


app = create_app()

async def worker(queue, inserter):
    while True:
        payload = await queue.get()
        try:
            await inserter(payload)
        finally:
            queue.task_done()

def make_sink(loop, queue):
    def submit(payload):
        loop.call_soon_threadsafe(queue.put_nowait, payload)
    return submit