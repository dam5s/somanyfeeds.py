import unittest

from backend.pkgs.feeds_data.feeds_repository import FeedsRepository
from backend_tests.pkgs.database_test_support.testing_database_template import create_testing_db


class TestFeedsRepository(unittest.TestCase):
    def test_find_all(self):
        db = create_testing_db()
        db.execute("truncate feeds")

        repo = FeedsRepository(db)

        record1 = repo.add("https://example.com/rss.xml")
        record2 = repo.add("https://example.org/feed")

        self.assertEqual([record1, record2], repo.find_all())
