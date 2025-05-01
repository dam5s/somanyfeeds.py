from contextlib import asynccontextmanager
from os import environ
from typing import AsyncGenerator

from fastapi import FastAPI

from backend.apps.api_server import health_routes
from backend.apps.api_server.periodic_job_runner import PeriodicJobRunner
from backend.pkgs.feeds_processing.feeds_processor import DefaultFeedsProcessor, FeedsProcessor


def float_from_env(name: str, fallback: float) -> float:
    string_value = environ.get(name, None)
    if string_value is None:
        return fallback
    return float(string_value)


def build_app_from_env() -> FastAPI:
    return build_app(
        feeds_processor=DefaultFeedsProcessor(),
        feeds_processing_frequency=float_from_env("FEEDS_PROCESSING_FREQUENCY", fallback=5 * 60),
    )


def build_app(feeds_processor: FeedsProcessor, feeds_processing_frequency: float) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        runner = PeriodicJobRunner(
            job=feeds_processor.process_feeds_async,
            frequency=feeds_processing_frequency,
        )
        await runner.start_async()
        yield
        await runner.stop_async()

    api = FastAPI(lifespan=lifespan)
    api.include_router(health_routes.router(), prefix="/api")

    return api
