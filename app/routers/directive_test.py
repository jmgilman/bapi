from functools import lru_cache
from ..dependencies import BeanFile, get_beanfile
from ..main import app
from fastapi.testclient import TestClient


@lru_cache
def override():
    return BeanFile("testing/static.beancount")


def test_directive():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive")
    assert response.status_code == 200
    assert len(response.json()) == 1587


def test_directive_open():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/open")
    assert response.status_code == 200
    assert len(response.json()) == 63


def test_directive_close():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/close")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_commodity():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/commodity")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_directive_pad():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/pad")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_balance():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/balance")
    assert response.status_code == 200
    assert len(response.json()) == 63


def test_directive_transaction():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/transaction")
    assert response.status_code == 200
    assert len(response.json()) == 798


def test_directive_note():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/note")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_event():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/event")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_directive_query():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/query")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_price():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/price")
    assert response.status_code == 200
    assert len(response.json()) == 648


def test_directive_document():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/document")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_custom():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/custom")
    assert response.status_code == 200
    assert len(response.json()) == 0
