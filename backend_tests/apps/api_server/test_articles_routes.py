import unittest

import responses

from backend.apps.api_server.app_dependencies import AppDependencies
from backend_tests.apps.api_server.testing_app_dependencies import build_test_client
from backend_tests.pkgs.feeds_test_support.feeds_resources import content_from_feed_resource


class TestArticlesRoutes(unittest.IsolatedAsyncioTestCase):
    @responses.activate
    async def test_find_all_articles(self) -> None:
        stubbed_rss_feed = content_from_feed_resource("blog.xml")
        responses.add("GET", "https://blog.damo.io/rss.xml", body=stubbed_rss_feed, status=200)

        deps = AppDependencies.defaults()
        deps.feeds_repository.add("https://blog.damo.io/rss.xml")

        await deps.feeds_job_runner.run_once_async()
        self.assertEqual(5, len(deps.articles_repository.find_all()))

        client = build_test_client(dependencies=deps)
        response = client.get("/api/articles")

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIsInstance(response_json, dict)

        articles_json = response_json.get("articles")
        self.assertIsInstance(articles_json, list)
        self.assertEqual(5, len(articles_json))

        first_article = articles_json[0]
        expected_first_article = {
            "feed_url": "https://blog.damo.io/rss.xml",
            "url": "https://blog.damo.io/posts/things-to-learn-in-react-redux",
            "title": "Things to learn in React and Redux",
            "content": '<p>There is a lot of "tutorials" out there teaching React and Redux.</p>',
            "published_at": "2022-02-20T21:52:00Z",
        }
        self.assertEqual(expected_first_article, first_article)
