import uuid
from dataclasses import dataclass

from backend.pkgs.database_support.database_gateway import DatabaseGateway
from backend.pkgs.database_support.uuid_generator import UUIDGenerator


@dataclass
class FeedRecord:
    id: uuid.UUID
    url: str


class FeedsRepository:
    def __init__(self, db: DatabaseGateway, uuid_gen: UUIDGenerator):
        self.db = db
        self.uuid_gen = uuid_gen

    def add(self, url: str) -> FeedRecord:
        new_record_id = self.uuid_gen.generate()
        record = FeedRecord(id=new_record_id, url=url)
        self.db.execute("insert into feeds (id, url) values (%(id)s, %(url)s)", id=record.id.__str__(), url=record.url)
        return record

    def find_all(self) -> list[FeedRecord]:
        return self.db.query_all_records("select * from feeds", FeedRecord)
