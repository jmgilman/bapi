import pickle

from .redis import RedisStorage, RedisConfig
from ..settings import Settings
from unittest import mock


@mock.patch("beancount.loader.load_string")
@mock.patch("redis.StrictRedis.get")
def test_load(get, loader):
    contents = (["dirs"], ["errors"], {"opt": "value"})

    get.return_value = b"test"
    loader.return_value = contents

    settings = Settings()
    settings.redis = RedisConfig()
    storage = RedisStorage(settings)
    result = storage.load()

    assert result.entries == contents[0]
    assert result.errors == contents[1]
    assert result.options == contents[2]
    get.assert_called_once_with(settings.redis.key)
    loader.assert_called_once_with("test")

    get.return_value = pickle.dumps(contents)
    settings.redis.cached = True
    storage = RedisStorage(settings)
    result = storage.load()

    assert result.entries == contents[0]
    assert result.errors == contents[1]
    assert result.options == contents[2]
