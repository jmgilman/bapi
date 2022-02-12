import asyncio
import cachetools

from .base import BaseStorage
from anyio import Lock
from bdantic import models
from dataclasses import dataclass
from loguru import logger


@dataclass
class Cache(cachetools.Cache):
    """A cache for storing a `BeancountFile`.

    This class provides global access to a cached instance of `BeancountFile`
    which can be reused across requests. An invalidator method is automatically
    run on startup and is responsible for invalidating request when the
    underlying storage changes.

    Attributes:
        interval: Frequency that the invalidator should check the storage.
        storage: The underlying storage being used.

    """

    interval: int
    lock: Lock
    storage: BaseStorage
    _value: models.BeancountFile

    def __init__(self, storage: BaseStorage, interval: int = 5):
        super().__init__(50)
        self.storage = storage
        self.interval = interval
        self.lock = Lock()

    async def beanfile(self) -> models.BeancountFile:
        async with self.lock:
            return self["beanfile"]

    async def load(self):
        logger.info("Loading cache data")
        async with self.lock:
            self["beanfile"] = self.storage.load()
        logger.info("Cache data successfully loaded")

    async def background(self):
        """An async loop for managing the cache."""
        # Prime the cache
        logger.info("Priming cache")
        await self.load()

        logger.info("Entering main cache loop")
        while True:
            # Check for state changes
            if self.storage.changed(self["beanfile"]):
                logger.info("Cache invalidated")
                await self.load()

            await asyncio.sleep(self.interval)
