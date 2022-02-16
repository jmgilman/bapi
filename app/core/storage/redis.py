import redis
from bdantic import models
from beancount import loader
from loguru import logger
from pydantic import BaseModel

from app.core import base


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


class RedisStorage(base.BaseStorage):
    """Provides an interface for loading ledgers stored in Redis."""

    def __init__(self, settings):
        super().__init__(settings)

        self.host = self.settings.redis.host
        self.port = self.settings.redis.port
        self.password = self.settings.redis.password
        self.channel = self.settings.redis.channel
        self.ssl = self.settings.redis.ssl

        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            ssl=self.ssl,
        )

    def load(self) -> models.BeancountFile:
        assert self.settings.redis is not None
        logger.info(f"Using Redis server at {self.host}:{self.port}")

        logger.info(f"Subscribing to {self.channel} channel for updates")
        try:
            self.sub = self.client.pubsub()
            self.sub.subscribe(self.channel)
        except redis.exceptions.ConnectionError as e:
            raise base.StorageLoadError(
                f"Failed subscribing to channel: {str(e)}"
            )

        logger.info(f"Reading data from `{self.settings.redis.key}` key")
        try:
            contents = self.client.get(self.settings.redis.key)
        except redis.exceptions.ConnectionError as e:
            raise base.StorageLoadError(f"Failed reading data: {str(e)}")

        if self.settings.redis.cached:
            logger.info("Decompressing pickled data")
            return models.BeancountFile.decompress(contents)
        else:
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
