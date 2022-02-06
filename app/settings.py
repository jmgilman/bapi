import os

from enum import Enum
from functools import cached_property
from .internal.beancount import BeancountFile
from .internal.storage import BaseStorage
from .internal.providers.storage.local import LocalStorage
from .internal.providers.storage.s3 import S3Config, S3Storage
from pydantic import BaseSettings, BaseModel
from typing import Dict, Optional, Type


class Storage(str, Enum):
    local = "local"
    s3 = "s3"


class Auth(str, Enum):
    none = "none"
    jwt = "jwt"


class JWT(BaseModel):
    """Configuration class for configuring JWT authentication

    Attributes:
        algorithms: A comma separated list of approved algorithms to use
        audience: The API audience
        jwks: The URL to a JWKS endpoint for fetching keys
        issuer: The token issuer
    """

    algorithms: str = "RS256"
    audience: str = ""
    jwks: str = ""
    issuer: str = ""


class Settings(BaseSettings):
    """Main configuration class for the API server.

    Attributes:
        entrypoint: The filename of the main ledger file to parse.
        work_dir: The local working directory where files will be downloaded.
        strorage: Where to find Beancount files - local filesystem or Amazon S3
        auth: Type of authentication to use on endpoints - none or JWT
        jwt: Settings for configuring JWT authentication
        s3: Settings for configuring Amazon S3 storage
    """

    entrypoint: str = "main.beancount"
    work_dir: str = "/tmp/bean"
    storage: Storage = Storage.local
    auth: Auth = Auth.none
    jwt: Optional[JWT] = None
    s3: Optional[S3Config] = None

    _storage_providers: Dict[Storage, Type[BaseStorage]] = {
        Storage.local: LocalStorage,
        Storage.s3: S3Storage,
    }

    class Config:
        env_prefix = "BAPI_"
        env_nested_delimiter = "__"
        keep_untouched = (cached_property,)

    @cached_property
    def beanfile(self) -> BeancountFile:
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
        print("LOADING!")
        return self._storage_providers[self.storage](self).load()

    def entry_path(self):
        """Returns the full path to the entrypoint beancount file.

        Returns:
            The path to the entrypoint beancount file.
        """
        return os.path.join(self.work_dir, self.entrypoint)


# Load settings
settings: Settings = Settings()
