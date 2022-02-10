import asyncio

from .settings import Settings
from anyio import Lock

# Ensures requests wait during a cache reload
lock = Lock()


class CacheInvalidator:
    """A background task for automatically invalidating the cache."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def main(self):
        """A async task which checks and refreshes the `BeancountFile` cache.

        Args:
            wait_time: The time (in seconds) to wait between checks.
        """
        while True:
            if self.settings.cache_invalidated():
                async with lock:
                    del self.settings.beanfile
                    self.settings.beanfile

            await asyncio.sleep(self.settings.cache_interval)
