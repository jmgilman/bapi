from __future__ import annotations

import boto3  # type: ignore
import os

from ...beancount import BeancountFile, from_file
from pathlib import Path
from pydantic import BaseModel
from ...storage import BaseStorage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....settings import Settings


class S3Config(BaseModel):
    """Configuration class for Amazon S3 support.

    Attributes:
        bucket: The S3 bucket name to download ledger files from
    """

    bucket: str = ""


class S3Storage(BaseStorage):
    """Provides an interface for downloading Beancount ledger files from Amazon S3.

    This class expects the main ledger file as well as all supporting ledger
    files to be contained within a single S3 bucket. No filtering is done when
    inspecting the bucket and therefore all files contained within the bucket
    will be downloaded to the working directory specified via the settings.
    """

    def __init__(self, settings: Settings):
        super().__init__(settings)

        if self.settings.s3 is None:
            raise InvalidS3Settings("Must set environment variables for S3")
        elif self.settings.s3.bucket is None:
            raise InvalidS3Settings(
                "Must set the S3 bucket environment variable"
            )

        self.bucket = boto3.resource("s3").Bucket(self.settings.s3.bucket)

    def load(self) -> BeancountFile:
        Path(self.settings.work_dir).mkdir(parents=True, exist_ok=True)
        for object in self.bucket.objects.all():
            self._download(object.key)

        return from_file(self.settings.entry_path())

    def _download(self, key: str):
        """Downloads the given object to the configured working directory.

        Args:
            key: The key of the object to download
        """
        file_path = os.path.join(self.settings.work_dir, key)
        file_dir = os.path.dirname(file_path)

        Path(file_dir).mkdir(parents=True, exist_ok=True)
        self.bucket.download_file(key, file_path)


class InvalidS3Settings(Exception):
    pass
