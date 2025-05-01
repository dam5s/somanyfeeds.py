from backend.apps.api_server.app_dependencies import AppDependencies
from backend.apps.api_server.feeds_processor import FeedsProcessor
from backend.pkgs.feeds_data.feeds_repository import FeedsRepository
from backend_tests.pkgs.feeds_processing.testing_feeds_processor import TestingFeedsProcessor


def build_testing_app_dependencies(
    feeds_repository: FeedsRepository = FeedsRepository(),
    feeds_processor: FeedsProcessor = TestingFeedsProcessor(),
    feeds_processing_frequency: float = 1.0,
) -> AppDependencies:
    return AppDependencies(
        feeds_repository=feeds_repository,
        feeds_processing_frequency=feeds_processing_frequency,
        feeds_processor=feeds_processor,
    )
