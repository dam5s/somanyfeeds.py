from dataclasses import dataclass

from backend.apps.api_server.feeds_processor import FeedsProcessor
from backend.pkgs.feeds_data.feeds_repository import FeedsRepository


@dataclass(frozen=True)
class AppDependencies:
    feeds_repository: FeedsRepository
    feeds_processor: FeedsProcessor
    feeds_processing_frequency: float
