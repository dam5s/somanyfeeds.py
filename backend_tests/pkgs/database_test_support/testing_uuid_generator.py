from uuid import UUID

from backend.pkgs.database_support.uuid_generator import UUIDGenerator


class TestingUUIDGenerator(UUIDGenerator):
    __uuids: list[UUID]

    def __init__(self, *uuids: UUID):
        self.__uuids = list(uuids)

    def generate(self) -> UUID:
        if len(self.__uuids) == 0:
            raise Exception("No UUID stubs available")

        return self.__uuids.pop(0)
