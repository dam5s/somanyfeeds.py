import unittest
from datetime import datetime

from backend.pkgs.feeds_processing.feed_parser import Feed, FeedArticle
from backend.pkgs.feeds_processing.rss_parser import RssParser
from backend_tests.pkgs.feeds_test_support.feeds_resources import download_from_feed_resource


class TestRssParser(unittest.TestCase):
    def test_try_parse__bluesky_feed(self):
        download = download_from_feed_resource("bluesky.xml")
        result = RssParser().try_parse(download)

        self.assertIsInstance(result, Feed)
        self.assertEqual(15, len(result.articles))

        last_article = result.articles[-1]
        expected_article = FeedArticle(
            url="https://bsky.app/profile/damo.io/post/3kplru3ozsm2v",
            title=None,
            content="Xcel Energy has cutoff our electricity for over 30 hours.",
            published_at=datetime.fromisoformat("2024-04-08T04:08:00+00:00"),
        )
        self.assertEqual(expected_article, last_article)

    def test_try_parse__blog_feed(self):
        download = download_from_feed_resource("blog.xml")
        result = RssParser().try_parse(download)

        self.assertIsInstance(result, Feed)
        self.assertEqual(5, len(result.articles))

        last_article = result.articles[0]
        expected_article = FeedArticle(
            url="https://blog.damo.io/posts/things-to-learn-in-react-redux",
            title="Things to learn in React and Redux",
            content='<p>There is a lot of "tutorials" out there teaching React and Redux.</p>',
            published_at=datetime.fromisoformat("2022-02-20T21:52:00+00:00"),
        )
        self.assertEqual(expected_article, last_article)

    def test_try_parse__invalid_xml(self):
        # not even xml
        pass

    def test_try_parse__unexpected_xml(self):
        # xml that is not RSS
        pass
