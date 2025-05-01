from contextlib import asynccontextmanager
from os import environ
from typing import AsyncGenerator

from fastapi import FastAPI

from backend.apps.api_server import health_routes
from backend.apps.api_server.app_dependencies import AppDependencies
from backend.apps.api_server.feeds_processor import DefaultFeedsProcessor
from backend.apps.api_server.periodic_job_runner import PeriodicJobRunner
from backend.pkgs.feeds_data.articles_repository import ArticlesRepository
from backend.pkgs.feeds_data.feeds_repository import FeedsRepository
from backend.pkgs.feeds_processing.feed_parser import MultiFeedParser
from backend.pkgs.feeds_processing.rss_parser import RssParser


def float_from_env(name: str, fallback: float) -> float:
    string_value = environ.get(name, None)
    if string_value is None:
        return fallback
    return float(string_value)


def dependencies_from_env() -> AppDependencies:
    feeds_repository = FeedsRepository()
    articles_repository = ArticlesRepository()
    feed_parser = MultiFeedParser(
        [
            RssParser(),
        ]
    )

    return AppDependencies(
        feeds_repository=feeds_repository,
        feeds_processor=DefaultFeedsProcessor(feeds_repository, articles_repository, feed_parser),
        feeds_processing_frequency=float_from_env("FEEDS_PROCESSING_FREQUENCY", fallback=5 * 60),
    )


def build_app(deps: AppDependencies = dependencies_from_env()) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        runner = PeriodicJobRunner(
            job=deps.feeds_processor.process_feeds_async,
            frequency=deps.feeds_processing_frequency,
        )
        await runner.start_async()
        yield
        await runner.stop_async()

    api = FastAPI(lifespan=lifespan)
    api.include_router(health_routes.router(), prefix="/api")

    return api
