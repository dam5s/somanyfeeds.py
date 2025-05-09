from dataclasses import dataclass

from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.apps.api_server.feeds_processor import FeedsProcessor
from backend.apps.api_server.periodic_job_runner import PeriodicJobRunner
from backend.pkgs.feeds_data.articles_repository import ArticlesRepository
from backend.pkgs.feeds_data.feeds_repository import FeedsRepository
from backend.pkgs.feeds_processing.feed_parser import MultiFeedParser, FeedParser
from backend.pkgs.feeds_processing.rss_parser import RssParser


class AppSettings(BaseSettings):
    feeds_processing_frequency: float = 5 * 60

    model_config = SettingsConfigDict(case_sensitive=False)


@dataclass(frozen=True)
class AppDependencies:
    articles_repository: ArticlesRepository
    feeds_repository: FeedsRepository
    feeds_job_runner: PeriodicJobRunner

    @staticmethod
    def default_feed_parser() -> FeedParser:
        return MultiFeedParser(
            [
                RssParser(),
            ]
        )

    @staticmethod
    def defaults(settings: AppSettings = AppSettings()) -> "AppDependencies":
        feeds_repository = FeedsRepository()
        articles_repository = ArticlesRepository()
        feed_parser = AppDependencies.default_feed_parser()
        feeds_processor = FeedsProcessor(feeds_repository, articles_repository, feed_parser)

        print(f"Loading app dependencies... frequency:{settings.feeds_processing_frequency}")

        return AppDependencies(
            articles_repository=articles_repository,
            feeds_repository=feeds_repository,
            feeds_job_runner=PeriodicJobRunner(job=feeds_processor, frequency=settings.feeds_processing_frequency),
        )
