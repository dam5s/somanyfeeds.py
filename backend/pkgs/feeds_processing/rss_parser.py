from datetime import datetime
from xml.etree.ElementTree import XML, Element

from backend.pkgs.feeds_processing.downloads import Download
from backend.pkgs.feeds_processing.feed_parser import FeedParser, ParseFeedFailure, Feed, FeedArticle


class RssParser(FeedParser):
    def try_parse(self, download: Download) -> Feed | ParseFeedFailure:
        tree = XML(download.content)
        items = tree.findall("channel/item")

        articles = [parse_item(item) for item in items]

        return Feed(articles)


def parse_item(item: Element) -> FeedArticle:
    date_format = "%d %b %Y %H:%M %z"  # 08 Apr 2024 04:08 +0000
    link_text = find_text(item, "link")
    description_text = find_text(item, "description")
    date_string = find_text(item, "pubDate")

    return FeedArticle(
        url=link_text,
        title=None,
        content=description_text,
        published_at=datetime.strptime(date_string, date_format),
    )


def find_text(element: Element, name: str) -> str:
    child = element.find(name)
    if child is None:
        return ""
    return child.text or ""
