import redis

from ..base import BaseStorage, ValidationError
from beancount import loader
from bdantic import models
from pydantic import BaseModel


class RedisConfig(BaseModel):
    """Configuration class for Redis support.

    Attributes:
        key: The key to load the data from
        cached: Whether the data is a pickled cache or raw ledger contents
        host: The redis database host
        port: The redis database port
        password: The redis database password
        ssl: Whether to use SSL or not
    """

    key: str = "beancount"
    cached: bool = False
    host: str = "localhost"
    port: int = 6379
    password: str = ""
    ssl: bool = True


class RedisStorage(BaseStorage):
    """Provides an interface for loading ledgers stored in Redis."""

    def load(self) -> models.BeancountFile:
        assert self.settings.redis is not None
        client = redis.Redis(
            host=self.settings.redis.host,
            port=self.settings.redis.port,
            password=self.settings.redis.password,
            ssl=self.settings.redis.ssl,
        )

        if self.settings.redis.cached:
            cached = client.get(self.settings.redis.key)
            if not cached:
                raise Exception(
                    "Redis returned no data with the configured key"
                )
            return models.BeancountFile.decompress(cached)
        else:
            contents = client.get(self.settings.redis.key)
            if not contents:
                raise Exception(
                    "Redis returned no data with the configured key"
                )

            return models.BeancountFile.parse(
                loader.load_string(contents.decode("utf-8"))
            )

    @classmethod
    def changed(cls, _: models.BeancountFile) -> bool:
        # TODO: Add support for cache invalidation
        return False

    @staticmethod
    def validate(settings) -> None:
        if settings.redis is None:
            raise ValidationError("Must set environment variables for Redis")
