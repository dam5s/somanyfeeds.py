from typing import Any, TypeVar, Type, cast

import dacite
from dacite.data import Data
from psycopg_pool import ConnectionPool

T = TypeVar("T")

DatabaseRow = dict[str, Any]


class NoResultFound(Exception):
    pass


def map_data_class(data_class: Type[T], row: DatabaseRow) -> T:
    return dacite.from_dict(data_class, cast(Data, row))


class DatabaseGateway:
    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    def execute(self, query: str, **kwargs: Any) -> None:
        with self.pool.connection() as connection:
            connection.execute(query, params=kwargs)

    def query_all_rows(self, query: str, **kwargs: Any) -> list[DatabaseRow]:
        with self.pool.connection() as connection:
            cursor = connection.execute(query, params=kwargs)
            return cursor.fetchall()

    def try_query_one_row(self, query: str, **kwargs: Any) -> DatabaseRow | None:
        rows = self.query_all_rows(query, **kwargs)

        if len(rows) < 1:
            return None

        return rows[0]

    def query_one_row(self, query: str, **kwargs: Any) -> DatabaseRow:
        row = self.try_query_one_row(query, **kwargs)

        if row is None:
            raise NoResultFound

        return row

    def query_all_records(self, query: str, data_class: Type[T], **kwargs: Any) -> list[T]:
        rows = self.query_all_rows(query, **kwargs)
        return [map_data_class(data_class, row) for row in rows]

    def query_one_record(self, query: str, data_class: Type[T], **kwargs: Any) -> T:
        row = self.query_one_row(query, **kwargs)
        return map_data_class(data_class, row)

    def try_query_one_record(self, query: str, data_class: Type[T], **kwargs: Any) -> T | None:
        row = self.try_query_one_row(query, **kwargs)

        if row is None:
            return None

        return map_data_class(data_class, row)
