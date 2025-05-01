from dataclasses import dataclass


@dataclass(frozen=True)
class FeedRecord:
    id: str
    url: str


class FeedsRepository:
    __feeds: list[FeedRecord] = []

    def add(self, record: FeedRecord) -> None:
        self.__feeds.append(record)

    def find_all(self) -> list[FeedRecord]:
        return self.__feeds.copy()
