"""create articles table

Revision ID: cb5a4bece4f2
Revises: e1b7008039d0
Create Date: 2025-05-14 11:06:01.460556

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'cb5a4bece4f2'
down_revision: Union[str, None] = 'e1b7008039d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        create table articles
        (
            id  uuid not null primary key,
            feed_url varchar(255) not null,
            url varchar(255) not null,
            title text null,
            content text not null,
            published_at timestamp
        );
        create index articles_feed_url on articles(feed_url);
        create unique index articles_url_feed_url on articles(feed_url, url);
        grant all privileges on table articles to somanyfeeds;
    """)
