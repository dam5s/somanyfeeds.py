import logging

from backend.apps.api_server.periodic_job_runner import AsyncJob
from backend.pkgs.feeds_data.articles_repository import ArticlesRepository, ArticleRecord
from backend.pkgs.feeds_data.feeds_repository import FeedsRepository, FeedRecord
from backend.pkgs.feeds_processing.downloads import download, DownloadFailure
from backend.pkgs.feeds_processing.feed_parser import ParseFeedFailure, Feed, FeedParser


class FeedsProcessor(AsyncJob):
    __feeds_repo: FeedsRepository
    __articles_repo: ArticlesRepository
    __feed_parser: FeedParser

    def __init__(self, feeds_repo: FeedsRepository, articles_repo: ArticlesRepository, feed_parser: FeedParser) -> None:
        self.__feeds_repo = feeds_repo
        self.__articles_repo = articles_repo
        self.__feed_parser = feed_parser

    async def run_async(self) -> None:
        for feed in self.__feeds_repo.find_all():
            result = self.__process_feed(feed)

            match result:
                case DownloadFailure():
                    logging.exception("Error downloading feed %s", feed.url, result.exception)
                case ParseFeedFailure():
                    logging.error("Error parsing feed %s", feed.url)
                case Feed():
                    article_records = [
                        ArticleRecord(
                            feed_url=feed.url,
                            url=article.url,
                            title=article.title,
                            content=article.content,
                            published_at=article.published_at,
                        )
                        for article in result.articles
                    ]
                    self.__articles_repo.upsert_all(article_records)

    def __process_feed(self, feed: FeedRecord) -> DownloadFailure | ParseFeedFailure | Feed:
        download_result = download(feed.url)

        if isinstance(download_result, DownloadFailure):
            return download_result

        return self.__feed_parser.try_parse(download_result)
