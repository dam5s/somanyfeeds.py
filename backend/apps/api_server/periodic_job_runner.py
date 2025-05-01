import asyncio
from asyncio import Task
from typing import Optional, Callable, Awaitable


class PeriodicJobRunner:

    __job: Callable[[], Awaitable[None]]
    __frequency: float
    __running: bool = False
    __task: Optional[Task[None]] = None

    def __init__(self, job: Callable[[], Awaitable[None]], frequency: float):
        self.__job = job
        self.__frequency = frequency

    async def start_async(self) -> None:
        if self.__running:
            return

        self.__running = True
        self.__task = asyncio.create_task(self.__run_continuously())

    async def stop_async(self) -> None:
        if not self.__running:
            return

        self.__running = False

        if self.__task is None:
            return

        self.__task.cancel()

    def __should_keep_running(self) -> bool:
        if not self.__running:
            return False

        if not self.__task:
            return False

        return not self.__task.cancelled()

    async def __run_continuously(self) -> None:
        while self.__should_keep_running():
            await self.__job()
            await asyncio.sleep(self.__frequency)
