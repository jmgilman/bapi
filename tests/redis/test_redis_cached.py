import json

import pytest
import requests  # type: ignore
from bdantic import models
from conftest import REDIS_KEY, RedisContainer


@pytest.fixture
def cached() -> str:
    """Returns the cache mode for the API server. Can be overriden."""
    return "1"


@pytest.fixture
def migration(
    parsed_data: models.BeancountFile,
    redis_cont: RedisContainer,
):
    client = redis_cont.client()
    client.set(REDIS_KEY, parsed_data.compress())


def test_redis(app_url, parsed_data):
    # Test data was fetched from the Redis backend
    resp = requests.get(f"{app_url}/file").json()
    assert resp == json.loads(parsed_data.json())
