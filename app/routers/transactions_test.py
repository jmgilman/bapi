from functools import lru_cache
from ..dependencies import BeanFile, get_beanfile
from ..main import app
from fastapi.testclient import TestClient


@lru_cache
def override():
    return BeanFile("testing/static.beancount")


def test_directive_transaction():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/transaction")
    assert response.status_code == 200
    assert len(response.json()) == 798

    response = client.get("/transaction?account=Assets:US:Babble:Vacation")
    assert response.status_code == 200
    assert len(response.json()) == 56

    response = client.get("/transaction?start=2022-01-01")
    assert response.status_code == 200
    assert len(response.json()) == 20

    response = client.get("/transaction?end=2022-01-01")
    assert response.status_code == 200
    assert len(response.json()) == 778

    response = client.get("/transaction?search=Uncle%20Boons")
    assert response.status_code == 200
    assert len(response.json()) == 29
