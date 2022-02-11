import pytest

from testing import common as c


@pytest.fixture
def client():
    return c.client()


def test_realize(client):
    expected = c.load_realize_json()
    response = client.get("/realize")

    assert response.json() == expected
