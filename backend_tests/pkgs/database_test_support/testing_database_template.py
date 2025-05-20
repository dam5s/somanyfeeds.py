from backend.pkgs.database_support.connection_pool import create_connection_pool
from backend.pkgs.database_support.database_gateway import DatabaseGateway


def create_testing_db() -> DatabaseGateway:
    connection_pool = create_connection_pool(
        db_url="postgresql://somanyfeeds:secret@localhost/somanyfeeds_test",
        min_size=1,
        max_size=2,
    )
    return DatabaseGateway(connection_pool)
