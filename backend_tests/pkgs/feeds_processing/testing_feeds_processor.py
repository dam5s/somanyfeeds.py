from backend.apps.api_server.periodic_job_runner import AsyncJob


class TestingFeedsProcessor(AsyncJob):
    async def run_async(self) -> None:
        pass
