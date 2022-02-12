import redis

from ..base import BaseStorage
from beancount import loader
from bdantic import models
from loguru import logger
from pydantic import BaseModel


class RedisConfig(BaseModel):
    """Configuration class for Redis support.

    Attributes:
        key: The key to load the data from
        cached: Whether the data is a pickled cache or raw ledger contents
        channel: Channel to listen to for reloads
        host: The redis database host
        port: The redis database port
        password: The redis database password
        ssl: Whether to use SSL or not
    """

    key: str = "beancount"
    cached: bool = False
    channel: str = "beancount"
    host: str = "localhost"
    port: int = 6379
    password: str = ""
    ssl: bool = True


class RedisStorage(BaseStorage):
    """Provides an interface for loading ledgers stored in Redis."""

    def __init__(self, settings):
        super().__init__(settings)

        self.client = redis.Redis(
            host=self.settings.redis.host,
            port=self.settings.redis.port,
            password=self.settings.redis.password,
            ssl=self.settings.redis.ssl,
        )

    def load(self) -> models.BeancountFile:
        assert self.settings.redis is not None
        self.sub = self.client.pubsub()
        self.sub.subscribe(self.settings.redis.channel)

        if self.settings.redis.cached:
            logger.info(
                f"Reaching cached data from `{self.settings.redis.key}` key"
            )
            cached = self.client.get(self.settings.redis.key)
            if not cached:
                raise Exception(
                    "Redis returned no data with the configured key"
                )
            return models.BeancountFile.decompress(cached)
        else:
            logger.info(f"Reaching data from `{self.settings.redis.key}` key")
            contents = self.client.get(self.settings.redis.key)
            if not contents:
                raise Exception(
                    "Redis returned no data with the configured key"
                )

            return models.BeancountFile.parse(
                loader.load_string(contents.decode("utf-8"))
            )

    def changed(self, _: models.BeancountFile) -> bool:
        msg = self.sub.get_message()
        if msg:
            if msg["type"] == "message":
                return True
            else:
                return False
        else:
            return False
