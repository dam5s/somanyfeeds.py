from contextlib import asynccontextmanager
from os import environ
from typing import AsyncGenerator, Optional

from fastapi import FastAPI

from backend.apps.api_server import health_routes, articles_routes
from backend.apps.api_server.app_dependencies import AppDependencies


def float_from_env(name: str) -> Optional[float]:
    string_value = environ.get(name, None)
    if string_value is None:
        return None
    return float(string_value)


def dependencies_from_env() -> AppDependencies:
    return AppDependencies.defaults(feeds_processing_frequency=float_from_env("FEEDS_PROCESSING_FREQUENCY"))


def build_app(deps: AppDependencies = dependencies_from_env()) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        await deps.feeds_job_runner.start_async()
        yield
        await deps.feeds_job_runner.stop_async()

    api = FastAPI(lifespan=lifespan)
    api.include_router(health_routes.router(), prefix="/api")
    api.include_router(articles_routes.router(deps), prefix="/api")

    return api
