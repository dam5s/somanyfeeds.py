import unittest
import uuid

from backend.pkgs.feeds_data.feeds_repository import FeedsRepository
from backend_tests.pkgs.database_test_support.testing_database_template import create_testing_db
from backend_tests.pkgs.database_test_support.testing_uuid_generator import TestingUUIDGenerator


class TestFeedsRepository(unittest.TestCase):
    def test_find_all(self):
        db = create_testing_db()
        db.execute("truncate feeds")

        uuids = [uuid.uuid4(), uuid.uuid4()]
        uuid_gen = TestingUUIDGenerator(*uuids)
        repo = FeedsRepository(db, uuid_gen)

        record1 = repo.add("https://example.com/rss.xml")
        record2 = repo.add("https://example.org/feed")

        self.assertEqual([record1, record2], repo.find_all())
