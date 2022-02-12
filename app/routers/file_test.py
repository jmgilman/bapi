import pytest
from testing import common as c


@pytest.fixture
def client():
    return c.client()


def test_file(client):
    expected = c.load_file_json()
    response = client.get("/file")

    assert response.json() == expected


def test_errors(client):
    expected = []
    response = client.get("/file/errors")

    assert expected == response.json()


def test_options(client):
    expected = c.load_file_json()
    response = client.get("/file/options")

    assert expected["options"] == response.json()
