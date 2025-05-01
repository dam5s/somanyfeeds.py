from fastapi import FastAPI

from backend.apps.api_server.app import build_app
from backend.pkgs.feeds_processing.feeds_processor import FeedsProcessor
from backend_tests.pkgs.feeds_processing.testing_feeds_processor import TestingFeedsProcessor


def build_testing_app(
    feeds_processor: FeedsProcessor = TestingFeedsProcessor(),
    feeds_processing_frequency: float = 1.0,
) -> FastAPI:
    return build_app(feeds_processor=feeds_processor, feeds_processing_frequency=feeds_processing_frequency)
