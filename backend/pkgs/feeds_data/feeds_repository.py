import uuid
from dataclasses import dataclass

from backend.pkgs.database_support.database_template import DatabaseTemplate
from backend.pkgs.database_support.uuid_v7 import generate_uuid_v7


@dataclass(frozen=True)
class FeedRecord:
    id: uuid.UUID
    url: str


class FeedsRepository:
    def __init__(self, db: DatabaseTemplate):
        self.db = db

    def add(self, url: str) -> FeedRecord:
        record = FeedRecord(id=generate_uuid_v7(), url=url)
        self.db.execute("insert into feeds (id, url) values (:id, :url)", id=record.id.__str__(), url=record.url)
        return record

    def find_all(self) -> list[FeedRecord]:
        return self.db.query_all("select * from feeds", FeedRecord)
