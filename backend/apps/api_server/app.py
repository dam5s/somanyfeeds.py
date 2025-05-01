from contextlib import asynccontextmanager
from os import environ
from typing import AsyncGenerator

from fastapi import FastAPI

from backend.apps.api_server import hello_routes, health_routes
from backend.apps.api_server.feeds_processor import FeedsProcessor, DefaultFeedsProcessor
from backend.apps.api_server.periodic_job_runner import PeriodicJobRunner


def build_app_from_env() -> FastAPI:
    return build_app(
        feeds_processor=DefaultFeedsProcessor(),
        message=environ.get("MESSAGE", "Hello, World!"),
    )


def build_app(feeds_processor: FeedsProcessor, message: str) -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        runner = PeriodicJobRunner(
            job=feeds_processor.process_feeds_async,
            frequency=60 * 5 # 5 minutes
        )
        await runner.start_async()
        yield
        await runner.stop_async()

    api = FastAPI(lifespan=lifespan)
    api.include_router(hello_routes.router(message), prefix="/api")
    api.include_router(health_routes.router(), prefix="/api")

    return api
