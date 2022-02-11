import asyncio
from dataclasses import dataclass

from .base import BaseStorage
from anyio import Lock
from bdantic import models

# Ensures requests wait during a cache reload
lock = Lock()


@dataclass
class Cache:
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
    storage: BaseStorage
    _value: models.BeancountFile

    def __init__(self, storage: BaseStorage, interval: int = 5):
        self.storage = storage
        self.interval = interval
        self._value = storage.load()

    def get(self) -> models.BeancountFile:
        """Fetches the `BeancountInstance` from the cache.

        Returns:
            The cached `BeancountFile` instance.
        """
        return self._value

    async def invalidator(self):
        """An async loop for invalidating the cache on storage changes."""
        while True:
            if self.storage.changed(self._value):
                async with lock:
                    self._value = self.storage.load()

            await asyncio.sleep(self.interval)
