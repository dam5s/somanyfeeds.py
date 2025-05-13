import sqlalchemy

from backend.pkgs.database_support.database_template import DatabaseTemplate


def create_testing_db() -> DatabaseTemplate:
    engine = sqlalchemy.create_engine("postgresql://somanyfeeds:secret@localhost/somanyfeeds_test", pool_size=2)
    return DatabaseTemplate(engine)
