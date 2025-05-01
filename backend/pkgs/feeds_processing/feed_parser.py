from dataclasses import dataclass
from typing import Optional

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


def parse_feed(download: Download) -> Feed | ParseFeedFailure:
    return ParseFeedFailure(errors=[ParseError(message="Not implemented")])
