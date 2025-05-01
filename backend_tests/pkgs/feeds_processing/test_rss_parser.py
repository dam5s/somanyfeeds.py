import unittest
from datetime import datetime
from pathlib import Path

from backend.pkgs.feeds_processing.downloads import Download
from backend.pkgs.feeds_processing.feed_parser import Feed, FeedArticle
from backend.pkgs.feeds_processing.rss_parser import RssParser


def download_from_test_resource(file_name: str) -> Download:
    file_path = Path(__file__).parent / "resources" / file_name

    with open(file_path) as f:
        content = f.read()

    return Download(url=f"file://{file_name}", content=content)


class TestRssParser(unittest.TestCase):
    def test_try_parse(self) -> None:
        download = download_from_test_resource("bluesky.xml")
        result = RssParser().try_parse(download)

        self.assertIsInstance(result, Feed)
        self.assertEqual(15, len(result.articles))

        last_article = result.articles[-1]
        expected_article = FeedArticle(
            url="https://bsky.app/profile/damo.io/post/3kplru3ozsm2v",
            title=None,
            content="Xcel Energy has cutoff our electricity for over 30 hours.",
            published_at=datetime.fromisoformat("2024-04-08T04:08+00:00"),
        )
        self.assertEqual(expected_article, last_article)

    def test_try_parse__invalid_xml(self) -> None:
        # not even xml
        pass

    def test_try_parse__unexpected_xml(self) -> None:
        # xml that is not RSS
        pass
