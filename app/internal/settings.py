import os

from .base import BaseAuth, BaseStorage
from .auth.jwt import JWTAuth, JWTConfig
from .storage.local import LocalStorage
from .storage.redis import RedisConfig, RedisStorage
from .storage.s3 import S3Config, S3Storage
from enum import Enum
from bdantic import models
from functools import cached_property
from pydantic import BaseSettings
from typing import Dict, Optional, Type


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
        entrypoint: The filename of the main ledger file to parse.
        work_dir: The local working directory where files will be downloaded.
        storage: Where to find Beancount files
        auth: Type of authentication to use on endpoints
        jwt: Settings for configuring JWT authentication
        redis: Settings for configuring Redis storage
        s3: Settings for configuring Amazon S3 storage
    """

    entrypoint: str = "main.beancount"
    work_dir: str = "/tmp/bean"
    storage: Storage = Storage.local
    auth: Auth = Auth.none
    jwt: Optional[JWTConfig] = None
    redis: Optional[RedisConfig] = None
    s3: Optional[S3Config] = None

    _auth_providers: Dict[Auth, Type[BaseAuth]] = {Auth.jwt: JWTAuth}

    _storage_providers: Dict[Storage, Type[BaseStorage]] = {
        Storage.local: LocalStorage,
        Storage.redis: RedisStorage,
        Storage.s3: S3Storage,
    }

    class Config:
        env_prefix = "BAPI_"
        env_nested_delimiter = "__"
        keep_untouched = (cached_property,)

    @cached_property
    def beanfile(self) -> models.BeancountFile:
        """Returns the `BeancountFile` instance for the configured ledger.

        How and where the beancount ledger is loaded from is determined by the
        environment variables set during runtime. By default the storage is set
        to local and will attempt to load the contents of the file located at
        `{settings.work_dir}/{settings.entrypoint}`. Otherwise, the storage
        provider configured is loaded and passed an instance of the settings to
        perform whatever operation is necessary to return a `BeancountFile`.

        This property is configured to be cached to avoid loading the ledger
        more than once since it's a very expensive operation.

        Returns:
            A new `BeancountFile` instance with the configured ledger file.
        """
        return self._storage_providers[self.storage](self).load()

    def entry_path(self):
        """Returns the full path to the entrypoint beancount file.

        Returns:
            The path to the entrypoint beancount file.
        """
        return os.path.join(self.work_dir, self.entrypoint)

    def get_auth(self) -> Optional[BaseAuth]:
        """Returns the configured authentication provider, if any.

        Returns:
            The configured authenitcation provider or None.
        """
        return self._auth_providers[self.auth](self)

    def validate(self):
        """Validates this settings instance."""
        if self.auth is not Auth.none:
            self._auth_providers[self.auth].validate(self)

        self._storage_providers[self.storage].validate(self)


# Load settings
settings: Settings = Settings()
