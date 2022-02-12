from unittest import mock

from fastapi.testclient import TestClient


@mock.patch("bdantic.models.file.BeancountFile.query")
def test_query(query, client: TestClient, query_response):
    query.return_value = query_response
    response = client.get("/query?bql=test")

    assert response.json() == query_response
    query.assert_called_once_with("test")
