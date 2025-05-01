from dataclasses import dataclass
from typing import Optional, Protocol

from backend.pkgs.feeds_processing.downloads import Download


@dataclass(frozen=True)
class FeedArticle:
    url: str
    title: str
    content: str


@dataclass(frozen=True)
class ParseError:
    message: str
    exception: Optional[Exception] = None


@dataclass(frozen=True)
class Feed:
    articles: list[FeedArticle]


@dataclass(frozen=True)
class ParseFeedFailure:
    errors: list[ParseError]


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

            if isinstance(result, Feed):
                return result

            errors.extend(result.errors)

        return ParseFeedFailure(errors)
