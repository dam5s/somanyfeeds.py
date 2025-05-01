from datetime import datetime
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass(frozen=True)
class ArticleRecord:
    feed_url: str
    url: str
    title: Optional[str]
    content: str
    published_at: datetime

    def key(self) -> Tuple[str, str]:
        return self.feed_url, self.url


class ArticlesRepository:
    __articles: dict[Tuple[str, str], ArticleRecord] = {}

    def upsert(self, record: ArticleRecord) -> None:
        self.__articles[record.key()] = record

    def find_all(self) -> list[ArticleRecord]:
        return list(self.__articles.values())

    def upsert_all(self, records: list[ArticleRecord]) -> None:
        for record in records:
            self.upsert(record)
