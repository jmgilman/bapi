import os

import pytest
import redis
import requests  # type: ignore
from bdantic import models
from beancount import loader
from pytest_docker_tools import wrappers  # type: ignore
from pytest_docker_tools import build, container, fetch, network

REDIS_KEY = "beancount"


class BeanExampleContainer(wrappers.Container):
    """Wraps the bean_example container."""

    def data(self) -> str:
        """Fetches the generated beancount data from the container.

        Returns:
            The generated beancount data.
        """
        ip, port = self.get_addr("8001/tcp")
        return requests.get(f"http://{ip}:{port}/").text


class RedisContainer(wrappers.Container):
    """Wraps the redis container."""

    def client(self) -> redis.Redis:
        """Creates a new Redis client configured to use this container.

        Returns:
            A configured Redis client."""
        ip, port = self.get_addr("6379/tcp")
        return redis.Redis(host=ip, port=port)


# Place all containers on the same network for DNS support
test_network = network(scope="session")

# A small container which serves random beancount data over HTTP
bexample_image = fetch(repository="ghcr.io/jmgilman/beancount-example:latest")
bexample_cont = container(
    image="{bexample_image.id}",
    name="bean_example",
    ports={"8001/tcp": None},
    network="{test_network.name}",
    wrapper_class=BeanExampleContainer,
    scope="session",
)

# A redis container to serve as the storage backend
redis_image = fetch(repository="redis:latest")
redis_cont = container(
    image="{redis_image.id}",
    name="redis",
    ports={"6379/tcp": "6379"},
    network="{test_network.name}",
    wrapper_class=RedisContainer,
)

# The API container
app_image = build(path=os.getcwd())
app_cont = container(
    image="{app_image.id}",
    name="bapi",
    ports={
        "8000/tcp": None,
    },
    network="{test_network.name}",
    environment={
        "BAPI_STORAGE": "redis",
        "BAPI_REDIS__HOST": "redis",
        "BAPI_REDIS__PORT": "6379",
        "BAPI_REDIS__KEY": REDIS_KEY,
        "BAPI_REDIS__CACHED": "{cached}",
        "BAPI_REDIS__SSL": "0",
    },
)


@pytest.fixture
def cached() -> str:
    """Returns the cache mode for the API server. Can be overriden."""
    return "0"


@pytest.fixture
def data(bexample_cont: BeanExampleContainer) -> str:
    """Returns the test beancount data being used across the session."""
    return bexample_cont.data()


@pytest.fixture
def parsed_data(data: str) -> models.BeancountFile:
    """Returns a parsed version of the data being used across the session."""
    return models.BeancountFile.parse(loader.load_string(data))


@pytest.fixture
def migration(
    data: str,
    redis_cont: RedisContainer,
):
    """Writes the random beancount data to the Redis backend."""
    client = redis_cont.client()
    client.set(REDIS_KEY, data.encode("utf-8"))


@pytest.fixture
def app_url(migration, app_cont):
    """Returns the URL of the API server."""
    ip, port = app_cont.get_addr("8000/tcp")
    url = f"http://{ip}:{port}/v1"
    print(app_cont.logs())
    return url
