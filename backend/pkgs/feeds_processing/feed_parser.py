from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Protocol

from backend.pkgs.feeds_processing.downloads import Download


@dataclass(frozen=True)
class FeedArticle:
    url: str
    title: Optional[str]
    content: str
    published_at: datetime


@dataclass(frozen=True)
class ParseError:
    message: str
    exception: Optional[Exception] = None

    @staticmethod
    def from_exception(exception: Exception) -> "ParseError":
        return ParseError(message="An exception occurred", exception=exception)


@dataclass(frozen=True)
class Feed:
    articles: list[FeedArticle]


@dataclass(frozen=True)
class ParseFeedFailure:
    errors: list[ParseError]

    @staticmethod
    def from_exception(exception: Exception) -> "ParseFeedFailure":
        return ParseFeedFailure([ParseError.from_exception(exception)])


class FeedParser(Protocol):
    def try_parse(self, download: Download) -> Feed | ParseFeedFailure: ...


class MultiFeedParser(FeedParser):
    __parsers: list[FeedParser]

    def __init__(self, parsers: list[FeedParser]):
        self.__parsers = parsers

    def try_parse(self, download: Download) -> Feed | ParseFeedFailure:
        errors: list[ParseError] = []

        for parser in self.__parsers:
            result = parser.try_parse(download)

            match result:
                case Feed():
                    return result
                case ParseFeedFailure():
                    errors.extend(result.errors)

        return ParseFeedFailure(errors)
