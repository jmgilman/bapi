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


def test_directive_open_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/open",
        json={"date": "2022-01-01", "account": "Assets:Bank:Test"},
    )
    assert response.status_code == 200
    assert response.text == "2022-01-01 open Assets:Bank:Test\n"


def test_directive_close():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/close")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_close_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/close",
        json={"date": "2022-01-01", "account": "Assets:Bank:Test"},
    )
    assert response.status_code == 200
    assert response.text == "2022-01-01 close Assets:Bank:Test\n"


def test_directive_commodity():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/commodity")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_directive_commodity_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/commodity",
        json={"date": "2022-01-01", "currency": "USD"},
    )
    assert response.status_code == 200
    assert response.text == "2022-01-01 commodity USD\n"


def test_directive_pad():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/pad")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_pad_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/pad",
        json={
            "date": "2022-01-01",
            "account": "Assets:Bank:Test1",
            "source_account": "Assets:Bank:Test2",
        },
    )
    assert response.status_code == 200
    assert (
        response.text == "2022-01-01 pad Assets:Bank:Test1 Assets:Bank:Test2\n"
    )


def test_directive_balance():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/balance")
    assert response.status_code == 200
    assert len(response.json()) == 63


def test_directive_balance_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/balance",
        json={
            "date": "2022-01-01",
            "account": "Assets:Bank:Test",
            "amount": {
                "number": 1234.56,
                "currency": "USD",
            },
        },
    )
    assert response.status_code == 200
    assert (
        response.text
        == "2022-01-01 balance Assets:Bank:Test" + (" " * 32) + "1234.56 USD\n"
    )


def test_directive_transaction():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/transaction")
    assert response.status_code == 200
    assert len(response.json()) == 798


def test_directive_transaction_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/transaction",
        json={
            "date": "2022-01-01",
            "flag": "*",
            "payee": "Payee",
            "narration": "Narration",
            "postings": [
                {
                    "account": "Assets:Bank:Test",
                    "units": {
                        "number": 1234.56,
                        "currency": "USD",
                    },
                },
                {
                    "account": "Expenses:Test",
                },
            ],
        },
    )
    assert response.status_code == 200
    assert response.text == (
        '2022-01-01 * "Payee" "Narration"\n'
        "  Assets:Bank:Test  1234.56 USD\n"
        "  Expenses:Test\n"
    )


def test_directive_note():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/note")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_note_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/note",
        json={
            "date": "2022-01-01",
            "account": "Assets:Bank:Test",
            "comment": "Test comment",
        },
    )
    assert response.status_code == 200
    assert response.text == '2022-01-01 note Assets:Bank:Test "Test comment"\n'


def test_directive_event():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/event")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_directive_event_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/event",
        json={
            "date": "2022-01-01",
            "type": "Test",
            "description": "Test event",
        },
    )
    assert response.status_code == 200
    assert response.text == '2022-01-01 event "Test" "Test event"\n'


def test_directive_query():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/query")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_query_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/query",
        json={
            "date": "2022-01-01",
            "name": "Query",
            "query_string": "SELECT account",
        },
    )
    assert response.status_code == 200
    assert response.text == '2022-01-01 query "Query" "SELECT account"\n'


def test_directive_price():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/price")
    assert response.status_code == 200
    assert len(response.json()) == 648


def test_directive_price_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/price",
        json={
            "date": "2022-01-01",
            "currency": "USD",
            "amount": {
                "number": 1234.56,
                "currency": "USD",
            },
        },
    )
    assert response.status_code == 200
    assert (
        response.text == "2022-01-01 price USD" + (" " * 31) + "1234.56 USD\n"
    )


def test_directive_document():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/document")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_document_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/document",
        json={
            "date": "2022-01-01",
            "account": "Assets:Bank:Test",
            "filename": "test.doc",
        },
    )
    assert response.status_code == 200
    assert response.text == '2022-01-01 document Assets:Bank:Test "test.doc"\n'


def test_directive_custom():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/directive/custom")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_directive_custom_generate():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.post(
        "/directive/custom",
        json={
            "date": "2022-01-01",
            "type": "Test",
            "values": [
                {"type": "date", "value": "2022-01-01"},
                {
                    "type": "amount",
                    "value": {
                        "number": 1234.56,
                        "currency": "USD",
                    },
                },
            ],
        },
    )
    assert response.status_code == 200
    assert response.text == '2022-01-01 custom "Test" 2022-01-01 1234.56 USD\n'
