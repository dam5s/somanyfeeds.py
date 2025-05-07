from datetime import datetime
from typing import Optional
from xml.etree.ElementTree import XML, Element

from backend.pkgs.feeds_processing.downloads import Download
from backend.pkgs.feeds_processing.feed_parser import FeedParser, ParseFeedFailure, Feed, FeedArticle


class RssParser(FeedParser):
    def try_parse(self, download: Download) -> Feed | ParseFeedFailure:
        try:
            tree = XML(download.content)
            items = tree.findall("channel/item")

            articles = [parse_item(item) for item in items]

            return Feed(articles)
        except Exception as e:
            return ParseFeedFailure.from_exception(e)


def parse_item(item: Element) -> FeedArticle:
    title_text = try_find_text(item, "title")
    link_text = find_text(item, "link")
    description_text = find_text(item, "description")
    date_string = find_text(item, "pubDate")

    return FeedArticle(
        url=link_text,
        title=title_text,
        content=description_text,
        published_at=parse_date(date_string),
    )


def parse_date(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        date_format = "%d %b %Y %H:%M %z"  # e.g. 08 Apr 2024 04:08 +0000
        return datetime.strptime(value, date_format)


def try_find_text(element: Element, name: str) -> Optional[str]:
    child = element.find(name)
    if child is None:
        return None
    return child.text


def find_text(element: Element, name: str) -> str:
    return try_find_text(element, name) or ""
