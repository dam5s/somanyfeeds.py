import os

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise ValueError("DATABASE_URL environment variable is not set")

psycopg_db_url = database_url.replace("postgresql://", "postgresql+psycopg://")
config = context.config
config.set_main_option("sqlalchemy.url", psycopg_db_url)

connectable = engine_from_config(
    config.get_section(config.config_ini_section, {}),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

with connectable.connect() as connection:
    context.configure(connection=connection, target_metadata=None)

    with context.begin_transaction():
        context.run_migrations()
