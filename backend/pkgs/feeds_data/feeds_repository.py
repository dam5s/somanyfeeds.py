import uuid
from typing import Any

from pydantic import BaseModel

from backend.pkgs.database_support.database_gateway import DatabaseGateway
from backend.pkgs.database_support.uuid_v7 import generate_uuid_v7


class FeedRecord(BaseModel):
    id: uuid.UUID
    url: str


def map_feed_record(row: dict[str, Any]) -> FeedRecord:
    return FeedRecord.model_validate(row)


class FeedsRepository:
    def __init__(self, db: DatabaseGateway):
        self.db = db

    def add(self, url: str) -> FeedRecord:
        record = FeedRecord(id=generate_uuid_v7(), url=url)
        self.db.execute("insert into feeds (id, url) values (:id, :url)", id=record.id.__str__(), url=record.url)
        return record

    def find_all(self) -> list[FeedRecord]:
        return self.db.query_all("select * from feeds", map_feed_record)
