from backend.apps.api_server.feeds_processor import FeedsProcessor


class TestingFeedsProcessor(FeedsProcessor):
    async def process_feeds_async(self) -> None:
        pass
