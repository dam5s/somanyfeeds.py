from backend.pkgs.feeds_processing.feeds_processor import FeedsProcessor


class TestingFeedsProcessor(FeedsProcessor):
    async def process_feeds_async(self) -> None:
        pass
