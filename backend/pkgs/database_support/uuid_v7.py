from uuid import UUID

import uuid6


def generate_uuid_v7() -> UUID:
    return uuid6.uuid7()
