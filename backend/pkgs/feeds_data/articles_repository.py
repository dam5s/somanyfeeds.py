from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from backend.pkgs.database_support.database_gateway import DatabaseGateway
from backend.pkgs.database_support.uuid_generator import UUIDGenerator


@dataclass(frozen=True)
class ArticleFields:
    feed_url: str
    url: str
    title: Optional[str]
    content: str
    published_at: datetime


@dataclass(frozen=True)
class ArticleRecord(ArticleFields):
    id: UUID

    @staticmethod
    def from_fields(record_id: UUID, fields: ArticleFields):
        return ArticleRecord(id=record_id, **fields.__dict__)


class ArticlesRepository:

    def __init__(self, db: DatabaseGateway, uuid_gen: UUIDGenerator):
        self.db = db
        self.uuid_gen = uuid_gen

    def find_all(self) -> list[ArticleRecord]:
        return []

    def upsert(self, fields: ArticleFields) -> ArticleRecord:
        new_record_id = self.uuid_gen.generate()
        return ArticleRecord.from_fields(record_id=new_record_id, fields=fields)

    def upsert_all(self, records: list[ArticleFields]) -> None:
        pass
