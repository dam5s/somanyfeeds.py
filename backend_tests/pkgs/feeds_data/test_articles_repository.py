import unittest
import uuid
from datetime import datetime

from backend.pkgs.feeds_data.articles_repository import ArticlesRepository, ArticleFields
from backend_tests.pkgs.database_test_support.testing_database_template import create_testing_db
from backend_tests.pkgs.database_test_support.testing_uuid_generator import TestingUUIDGenerator


class TestArticlesRepository(unittest.TestCase):

    def test_upsert__with_no_previous_record(self):
        db = create_testing_db()
        db.execute("truncate articles")
        
        generated_id = uuid.uuid4()
        repo = ArticlesRepository(db, uuid_gen=TestingUUIDGenerator(generated_id))

        upserted_article = repo.upsert(ArticleFields(
            feed_url="https://example.com/rss.xml",
            url="https://example.com/articles/1",
            title="My Article",
            content="This is a great article",
            published_at=datetime.fromisoformat("2023-01-01T00:00:00Z")
        ))

        persisted_articles = repo.find_all()
        self.assertEqual(1, len(persisted_articles))
