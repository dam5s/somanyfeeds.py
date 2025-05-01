from typing import Protocol


class FeedsProcessor(Protocol):
    async def process_feeds_async(self) -> None:
        pass


class DefaultFeedsProcessor(FeedsProcessor):
    async def process_feeds_async(self) -> None:
        print("Processing feeds")
