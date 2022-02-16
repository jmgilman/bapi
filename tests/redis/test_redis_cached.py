import json

import pytest
import requests  # type: ignore
from bdantic import models
from conftest import REDIS_KEY, RedisContainer


@pytest.fixture
def cached() -> str:
    """Overrides the cache feature to enable it."""
    return "1"


@pytest.fixture
def migration(
    parsed_data: models.BeancountFile,
    redis_cont: RedisContainer,
):
    """Writes a pickled version of the beancount data to the Redis backend."""
    client = redis_cont.client()
    client.set(REDIS_KEY, parsed_data.compress())


def test_redis(app_url, parsed_data):
    resp = requests.get(f"{app_url}/file").json()
    assert resp == json.loads(parsed_data.json())
