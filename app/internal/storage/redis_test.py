from .redis import RedisStorage, RedisConfig
from ..settings import Settings
from unittest import mock


@mock.patch("bdantic.models.BeancountFile.parse")
@mock.patch("bdantic.models.BeancountFile.decompress")
@mock.patch("beancount.loader.load_string")
@mock.patch("redis.StrictRedis.get")
def test_load(get, loader, decompress, parse):
    contents = ([], [], {})

    get.return_value = b"test"
    loader.return_value = contents
    parse.return_value = "parsed"

    settings = Settings()
    settings.redis = RedisConfig()
    storage = RedisStorage(settings)
    result = storage.load()

    assert result == "parsed"
    get.assert_called_once_with(settings.redis.key)
    loader.assert_called_once_with("test")
    parse.assert_called_once_with(contents)

    # Cached
    get.return_value = "bytes"
    settings.redis.cached = True
    storage = RedisStorage(settings)
    result = storage.load()

    decompress.assert_called_once_with("bytes")
