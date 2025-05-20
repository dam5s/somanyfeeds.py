import secrets
import time
from typing import Protocol
from uuid import UUID


class UUIDGenerator(Protocol):
    def generate(self) -> UUID:
        ...


class UUID7Generator(UUIDGenerator):
    def generate(self) -> UUID:
        nanoseconds = time.time_ns()
        timestamp_ms = nanoseconds // 10 ** 6
        uuid_int = (timestamp_ms & 0xFFFFFFFFFFFF) << 80
        uuid_int |= secrets.randbits(76)
        return UUID(int=uuid_int, version=7)
