from unittest.mock import Mock, patch

import pytest
from app.core import settings
from app.core.storage import s3


@pytest.fixture
def mock_settings():
    return settings.Settings(
        entrypoint="test.beancount",
        s3=s3.S3Config(bucket="test"),
        work_dir="/run",
    )


@patch("pathlib.Path.mkdir")
@patch("pathlib.Path.__init__")
def test_download(path_init, _, mock_settings):
    bucket = Mock()
    loader = s3.S3Storage(mock_settings)
    loader.bucket = bucket

    path_init.return_value = None

    loader._download("test/key.file")
    path_init.assert_called_once_with("/run/test")
    bucket.download_file.assert_called_once_with(
        "test/key.file", "/run/test/key.file"
    )


@patch("app.core.beancount.from_file")
@patch("pathlib.Path.mkdir")
@patch("pathlib.Path.__init__")
def test_load(path_init, _, from_file, mock_settings):
    bucket = Mock()
    loader = s3.S3Storage(mock_settings)
    loader.bucket = bucket

    path_init.return_value = None
    from_file.return_value = "file"

    object = Mock()
    object.key = "test/key.file"
    bucket.objects.all.return_value = [object]

    loader.load()
    path_init.assert_any_call("/run")
    bucket.objects.all.assert_called_once()
    bucket.download_file.assert_called_once_with(
        "test/key.file", "/run/test/key.file"
    )
