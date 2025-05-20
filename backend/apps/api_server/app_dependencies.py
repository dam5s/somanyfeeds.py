from dataclasses import dataclass

from backend.apps.api_server.feeds_processor import FeedsProcessor
from backend.apps.api_server.periodic_job_runner import PeriodicJobRunner
from backend.pkgs.database_support.connection_pool import create_connection_pool
from backend.pkgs.database_support.database_gateway import DatabaseGateway
from backend.pkgs.database_support.uuid_generator import UUID7Generator
from backend.pkgs.env_support.environment_settings import StringSetting, FloatSetting
from backend.pkgs.feeds_data.articles_repository import ArticlesRepository
from backend.pkgs.feeds_data.feeds_repository import FeedsRepository
from backend.pkgs.feeds_processing.feed_parser import MultiFeedParser, FeedParser
from backend.pkgs.feeds_processing.rss_parser import RssParser


@dataclass(frozen=True)
class AppSettings:
    database_url: str = StringSetting.with_default("DATABASE_URL", default="postgresql://somanyfeeds:secret@localhost/somanyfeeds_dev")
    feeds_processing_frequency: float = FloatSetting.with_default("FEEDS_PROCESSING_FREQUENCY", default=5 * 60)


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
        connection_pool = create_connection_pool(settings.database_url, min_size=2, max_size=4)
        db = DatabaseGateway(connection_pool)
        uuid_gen = UUID7Generator()

        feeds_repository = FeedsRepository(db, uuid_gen)
        articles_repository = ArticlesRepository(db, uuid_gen)
        feed_parser = AppDependencies.default_feed_parser()
        feeds_processor = FeedsProcessor(feeds_repository, articles_repository, feed_parser)

        return AppDependencies(
            articles_repository=articles_repository,
            feeds_repository=feeds_repository,
            feeds_job_runner=PeriodicJobRunner(job=feeds_processor, frequency=settings.feeds_processing_frequency),
        )
