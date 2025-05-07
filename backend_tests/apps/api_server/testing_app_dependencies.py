from typing import Optional

from fastapi.testclient import TestClient

from backend.apps.api_server.app import build_app
from backend.apps.api_server.app_dependencies import AppDependencies
from backend.apps.api_server.periodic_job_runner import AsyncJob, PeriodicJobRunner
from backend.pkgs.feeds_data.articles_repository import ArticlesRepository
from backend.pkgs.feeds_data.feeds_repository import FeedsRepository
from backend_tests.pkgs.feeds_processing.testing_feeds_processor import TestingFeedsProcessor


def build_testing_app_dependencies(
    articles_repository: ArticlesRepository = ArticlesRepository(),
    feeds_repository: FeedsRepository = FeedsRepository(),
    feeds_processor: AsyncJob = TestingFeedsProcessor(),
    feeds_processing_frequency: float = 1.0,
) -> AppDependencies:
    return AppDependencies(
        articles_repository=articles_repository,
        feeds_repository=feeds_repository,
        feeds_job_runner=PeriodicJobRunner(
            job=feeds_processor,
            frequency=feeds_processing_frequency,
        ),
    )


def build_test_client(
    articles_repository: ArticlesRepository = ArticlesRepository(),
    feeds_repository: FeedsRepository = FeedsRepository(),
    feeds_processor: AsyncJob = TestingFeedsProcessor(),
    feeds_processing_frequency: float = 1.0,
    dependencies: Optional[AppDependencies] = None,
) -> TestClient:
    dependencies = dependencies or build_testing_app_dependencies(
        articles_repository,
        feeds_repository,
        feeds_processor,
        feeds_processing_frequency,
    )

    # pyrefly: ignore
    return TestClient(build_app(dependencies))
