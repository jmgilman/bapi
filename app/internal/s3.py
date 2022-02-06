import boto3  # type: ignore
import os

from pathlib import Path
from ..settings import Settings


class S3Loader:
    """Provides an interface for downloading Beancount ledger files from Amazon S3.

    This class expects the main ledger file as well as all supporting ledger
    files to be contained within a single S3 bucket. No filtering is done when
    inspecting the bucket and therefore all files contained within the bucket
    will be downloaded to the working directory specified via the settings.
    """

    def __init__(self, settings: Settings):
        assert settings.s3 is not None
        assert settings.s3.bucket is not None

        self.bucket = boto3.resource("s3").Bucket(settings.s3.bucket)
        self.settings = settings

    def load(self):
        """Downloads all S3 bucket contents to the configured directory."""
        Path(self.settings.work_dir).mkdir(parents=True, exist_ok=True)
        for object in self.bucket.objects.all():
            self._download(object.key)

    def _download(self, key: str):
        """Downloads the given object to the configured working directory.

        Args:
            key: The key of the object to download
        """
        file_path = os.path.join(self.settings.work_dir, key)
        file_dir = os.path.dirname(file_path)

        Path(file_dir).mkdir(parents=True, exist_ok=True)
        self.bucket.download_file(key, file_path)
