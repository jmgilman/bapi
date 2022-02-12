from fastapi.testclient import TestClient


def test_file(client: TestClient, raw_file):
    response = client.get("/file")
    assert response.json() == raw_file


def test_errors(client: TestClient):
    response = client.get("/file/errors")
    assert response.json() == []


def test_options(client: TestClient, raw_options):
    response = client.get("/file/options")
    assert response.json() == raw_options
