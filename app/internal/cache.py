import asyncio

from .settings import Settings
from anyio import Lock

# Ensures requests wait during a cache reload
lock = Lock()


class CacheInvalidator:
    """A background task for automatically invalidating the cache."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def main(self, wait_time=5):
        """A async task which checks and refreshes the `BeancountFile` cache.

        Args:
            wait_time: The time (in seconds) to wait between checks.
        """
        while True:
            if self.settings.cache_invalidated():
                async with lock:
                    print("Cache invalidated")
                    del self.settings.beanfile
                    self.settings.beanfile

            print("Sleeping")
            await asyncio.sleep(wait_time)
