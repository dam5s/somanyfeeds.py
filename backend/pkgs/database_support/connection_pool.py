from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


def create_connection_pool(db_url: str, min_size: int, max_size: int) -> ConnectionPool:
    return ConnectionPool(
        db_url,
        min_size=min_size,
        max_size=max_size,
        open=True,
        kwargs={"row_factory": dict_row}
    )
