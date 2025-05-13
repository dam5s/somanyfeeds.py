from typing import Any, TypeVar, Type, cast

import dacite
from dacite.data import Data
from sqlalchemy import Engine, text
from sqlalchemy.exc import NoResultFound

T = TypeVar("T")


def decode_data_class(data_class: Type[T], data: dict[str, Any]) -> T:
    return dacite.from_dict(data_class, cast(Data, data))


class DatabaseTemplate:
    def __init__(self, engine: Engine):
        self.engine = engine

    def query_one(self, query: str, data_class: Type[T], **kwargs: Any) -> T:
        records = self.__query(query, **kwargs)

        if len(records) < 1:
            raise NoResultFound

        return decode_data_class(data_class, records[0])

    def query_all(self, query: str, data_class: Type[T], **kwargs: Any) -> list[T]:
        records = self.__query(query, **kwargs)
        return [decode_data_class(data_class, record) for record in records]

    def execute(self, query: str, **kwargs: Any) -> None:
        with self.engine.begin() as connection:
            connection.execute(text(query), parameters=kwargs)

    def __query(self, query: str, **kwargs: Any) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            results = connection.execute(text(query), parameters=kwargs).all()

            return [{key: row._mapping[key] for key in row._mapping.keys()} for row in results]
