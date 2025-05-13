from typing import cast
from uuid import UUID

from uuid_extensions import uuid7


def generate_uuid_v7() -> UUID:
    return cast(UUID, uuid7())
