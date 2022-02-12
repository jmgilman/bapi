from unittest import mock

from app.core import settings
from app.core.storage.redis import RedisConfig, RedisStorage

import redis


@mock.patch("bdantic.models.BeancountFile.parse")
@mock.patch("bdantic.models.BeancountFile.decompress")
@mock.patch("beancount.loader.load_string")
@mock.patch("redis.StrictRedis.pubsub")
@mock.patch("redis.StrictRedis.get")
def test_load(get, pubsub, loader, decompress, parse):
    contents = ([], [], {})
    ps = mock.Mock(redis.client.PubSub)

    pubsub.return_value = ps
    get.return_value = b"test"
    loader.return_value = contents
    parse.return_value = "parsed"

    stgs = settings.Settings()
    stgs.redis = RedisConfig()
    storage = RedisStorage(stgs)
    result = storage.load()

    assert result == "parsed"
    ps.subscribe.assert_called_once_with(stgs.redis.channel)
    get.assert_called_once_with(stgs.redis.key)
    loader.assert_called_once_with("test")
    parse.assert_called_once_with(contents)

    # Cached
    get.return_value = "bytes"
    stgs.redis.cached = True
    storage = RedisStorage(stgs)
    result = storage.load()

    decompress.assert_called_once_with("bytes")
