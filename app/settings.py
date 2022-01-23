from enum import Enum
from lib2to3.pytree import Base
import os

from pydantic import BaseSettings, BaseModel
from typing import Optional


class Storage(Enum):
    local = "local"
    s3 = "s3"


class Auth(Enum):
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


class S3(BaseModel):
    """Configuration class for Amazon S3 support.

    Attributes:
        bucket: The S3 bucket name to download ledger files from
    """

    bucket: str = ""


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
    storage: Storage = "local"
    auth: Auth = "none"
    jwt: Optional[JWT] = None
    s3: Optional[S3] = None

    class Config:
        env_prefix = "BAPI_"
        env_nested_delimiter = "__"


settings = Settings()
bean_file = os.path.join(settings.work_dir, settings.entrypoint)
