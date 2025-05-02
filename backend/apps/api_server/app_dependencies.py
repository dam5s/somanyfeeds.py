from dataclasses import dataclass

from backend.apps.api_server.periodic_job_runner import AsyncJob
from backend.pkgs.feeds_data.feeds_repository import FeedsRepository


@dataclass(frozen=True)
class AppDependencies:
    feeds_repository: FeedsRepository
    feeds_processor: AsyncJob
    feeds_processing_frequency: float
