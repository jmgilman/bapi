import os
from enum import Enum
from functools import cached_property

from pydantic import BaseSettings, PrivateAttr

from app.core.auth.jwt import JWTAuth, JWTConfig
from app.core.base import BaseAuth, BaseStorage
from app.core.storage.local import LocalStorage
from app.core.storage.redis import RedisConfig, RedisStorage
from app.core.storage.s3 import S3Config, S3Storage


class Storage(str, Enum):
    """Valid storage types which can be used with the API."""

    local = "local"
    redis = "redis"
    s3 = "s3"


class Auth(str, Enum):
    """Valid authentication types which can be used with the API."""

    none = "none"
    jwt = "jwt"


class Settings(BaseSettings):
    """Main configuration class for the API server.

    Attributes:
        version: The API version to use
        entrypoint: The filename of the main ledger file to parse.
        work_dir: The local working directory where files will be downloaded.
        cache_interval: Seconds to wait before checking for data changes.
        storage: Where to find Beancount files.
        auth: type of authentication to use on endpoints.
        jwt: Settings for configuring JWT authentication.
        redis: Settings for configuring Redis storage.
        s3: Settings for configuring Amazon S3 storage.
    """

    version: str = "v1"
    entrypoint: str = "main.beancount"
    work_dir: str = "/tmp/bean"
    cache_interval: int = 5
    storage: Storage = Storage.local
    auth: Auth = Auth.none
    jwt: JWTConfig | None = None
    redis: RedisConfig | None = None
    s3: S3Config | None = None

    _auth: BaseAuth | None = PrivateAttr(None)
    _storage: BaseStorage = PrivateAttr()

    _auth_providers: dict[Auth, type[BaseAuth]] = {Auth.jwt: JWTAuth}

    _storage_providers: dict[Storage, type[BaseStorage]] = {
        Storage.local: LocalStorage,
        Storage.redis: RedisStorage,
        Storage.s3: S3Storage,
    }

    class Config:
        env_prefix = "BAPI_"
        env_nested_delimiter = "__"
        keep_untouched = (cached_property,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.auth is not Auth.none:
            self._auth = self._auth_providers[self.auth](self)

        self._storage = self._storage_providers[self.storage](self)

    def entry_path(self):
        """Returns the full path to the entrypoint beancount file.

        Returns:
            The path to the entrypoint beancount file.
        """
        return os.path.join(self.work_dir, self.entrypoint)

    def get_auth(self) -> BaseAuth | None:
        """Returns the configured authentication provider, if any.

        Returns:
            The configured authenitcation provider or None.
        """
        return self._auth

    def get_storage(self) -> BaseStorage:
        """Returns the configured storage provider.

        Returns:
            The configured storage provider.
        """
        return self._storage
