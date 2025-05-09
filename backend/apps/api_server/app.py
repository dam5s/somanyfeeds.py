from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from backend.apps.api_server import health_routes, articles_routes
from backend.apps.api_server.app_dependencies import AppDependencies


def build_app(deps: AppDependencies = AppDependencies.defaults()) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        await deps.feeds_job_runner.start_async()
        yield
        await deps.feeds_job_runner.stop_async()

    api = FastAPI(lifespan=lifespan)
    api.include_router(health_routes.router(), prefix="/api")
    api.include_router(articles_routes.router(deps), prefix="/api")

    return api
