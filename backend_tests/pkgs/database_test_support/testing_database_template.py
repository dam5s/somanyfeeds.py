import sqlalchemy

from backend.pkgs.database_support.database_gateway import DatabaseGateway


def create_testing_db() -> DatabaseGateway:
    engine = sqlalchemy.create_engine("postgresql://somanyfeeds:secret@localhost/somanyfeeds_test", pool_size=2)
    return DatabaseGateway(engine)
