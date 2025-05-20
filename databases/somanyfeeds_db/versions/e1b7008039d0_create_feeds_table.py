"""create feeds table

Revision ID: e1b7008039d0
Revises:
Create Date: 2025-05-12 08:20:18.956223

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e1b7008039d0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        create table feeds
        (
            id uuid not null primary key,
            url varchar(255) not null
        );
        grant all privileges on table feeds to somanyfeeds;
    """)
