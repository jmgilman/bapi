import boto3  # type: ignore
import os

from ..base import BaseStorage, ValidationError
from ..beancount import from_file
from bdantic import models
from pathlib import Path
from pydantic import BaseModel
from typing import Any


class S3Config(BaseModel):
    """Configuration class for Amazon S3 support.

    Attributes:
        bucket: The S3 bucket name to download ledger files from
    """

    bucket: str = ""


class S3Storage(BaseStorage):
    """Provides an interface for fetching Beancount ledger files from Amazon S3.

    This class expects the main ledger file as well as all supporting ledger
    files to be contained within a single S3 bucket. No filtering is done when
    inspecting the bucket and therefore all files contained within the bucket
    will be downloaded to the working directory specified via the settings.

    Attrs:
        bucket: An instance of a S3 bucket
    """

    bucket: Any = None

    def load(self) -> models.BeancountFile:
        assert self.settings.s3 is not None
        if not self.bucket:
            self.bucket = boto3.resource("s3").Bucket(self.settings.s3.bucket)

        Path(self.settings.work_dir).mkdir(parents=True, exist_ok=True)
        for object in self.bucket.objects.all():
            self._download(object.key)

        return from_file(self.settings.entry_path())

    @staticmethod
    def validate(settings) -> None:
        if settings.s3 is None:
            raise ValidationError("Must set environment variables for S3")
        elif not settings.s3.bucket:
            raise ValidationError(
                "Must set the S3 bucket environment variable"
            )

    def _download(self, key: str) -> None:
        """Downloads the given object to the configured working directory.

        Args:
            key: The key of the object to download
        """
        file_path = os.path.join(self.settings.work_dir, key)
        file_dir = os.path.dirname(file_path)

        Path(file_dir).mkdir(parents=True, exist_ok=True)
        self.bucket.download_file(key, file_path)
