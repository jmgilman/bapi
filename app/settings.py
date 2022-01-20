import os

from pydantic import BaseSettings, BaseModel
from typing import Optional


class S3(BaseModel):
    """Configuration class for Amazon S3 support.

    Attributes:
        bucket: The S3 bucket name to download ledger files from
    """

    bucket: str


class Settings(BaseSettings):
    """Main configuration class for the API server.

    Attributes:
        entrypoint: The filename of the main ledger file to parse.
        s3: Configuration details for Amazon S3
        work_dir: The local working directory where files will be downloaded.
    """

    entrypoint: str
    s3: S3
    work_dir: str = "/tmp/bean"

    class Config:
        env_prefix = "BAPI_"
        env_nested_delimiter = "__"


settings = Settings()
bean_file = os.path.join(settings.work_dir, settings.entrypoint)
