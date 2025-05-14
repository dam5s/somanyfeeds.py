from typing import Any, TypeVar, Callable

from sqlalchemy import Engine, text
from sqlalchemy.exc import NoResultFound

T = TypeVar("T")

DatabaseRow = dict[str, Any]


class DatabaseGateway:
    def __init__(self, engine: Engine):
        self.engine = engine

    def query_one(self, query: str, mapping: Callable[[DatabaseRow], T], **kwargs: Any) -> T:
        records = self.__query(query, **kwargs)

        if len(records) < 1:
            raise NoResultFound

        return mapping(records[0])

    def query_all(self, query: str, mapping: Callable[[DatabaseRow], T], **kwargs: Any) -> list[T]:
        records = self.__query(query, **kwargs)
        return [mapping(record) for record in records]

    def execute(self, query: str, **kwargs: Any) -> None:
        with self.engine.begin() as connection:
            connection.execute(text(query), parameters=kwargs)

    def __query(self, query: str, **kwargs: Any) -> list[DatabaseRow]:
        with self.engine.connect() as connection:
            results = connection.execute(text(query), parameters=kwargs).all()
            return [dict(row._mapping) for row in results]
