import jmespath  # type: ignore
import pytest

from ..dependencies import DirectiveType
from testing import common as c
from typing import Dict, Tuple


@pytest.fixture
def client():
    return c.client()


@pytest.fixture
def syntax() -> Dict[str, Tuple[Dict, str]]:
    return {
        "open": (
            {
                "ty": "Open",
                "id": "",
                "date": "2022-01-01",
                "account": "Assets:Bank:Test",
            },
            "2022-01-01 open Assets:Bank:Test\n",
        ),
        "close": (
            {
                "ty": "Close",
                "id": "",
                "date": "2022-01-01",
                "account": "Assets:Bank:Test",
            },
            "2022-01-01 close Assets:Bank:Test\n",
        ),
        "commodity": (
            {
                "ty": "Commodity",
                "id": "",
                "date": "2022-01-01",
                "currency": "USD",
            },
            "2022-01-01 commodity USD\n",
        ),
        "pad": (
            {
                "ty": "Pad",
                "id": "",
                "date": "2022-01-01",
                "account": "Assets:Bank:Test1",
                "source_account": "Assets:Bank:Test2",
            },
            "2022-01-01 pad Assets:Bank:Test1 Assets:Bank:Test2\n",
        ),
        "balance": (
            {
                "ty": "Balance",
                "id": "",
                "date": "2022-01-01",
                "account": "Assets:Bank:Test",
                "amount": {
                    "number": 1234.56,
                    "currency": "USD",
                },
            },
            "2022-01-01 balance Assets:Bank:Test"
            + (" " * 32)
            + "1234.56 USD\n",
        ),
        "transaction": (
            {
                "ty": "Transaction",
                "id": "",
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
            '2022-01-01 * "Payee" "Narration"\n'
            "  Assets:Bank:Test  1234.56 USD\n"
            "  Expenses:Test\n",
        ),
        "note": (
            {
                "ty": "Note",
                "id": "",
                "date": "2022-01-01",
                "account": "Assets:Bank:Test",
                "comment": "Test comment",
            },
            '2022-01-01 note Assets:Bank:Test "Test comment"\n',
        ),
        "event": (
            {
                "ty": "Event",
                "id": "",
                "date": "2022-01-01",
                "type": "Test",
                "description": "Test event",
            },
            '2022-01-01 event "Test" "Test event"\n',
        ),
        "query": (
            {
                "ty": "Query",
                "id": "",
                "date": "2022-01-01",
                "name": "Query",
                "query_string": "SELECT account",
            },
            '2022-01-01 query "Query" "SELECT account"\n',
        ),
        "price": (
            {
                "ty": "Price",
                "id": "",
                "date": "2022-01-01",
                "currency": "USD",
                "amount": {
                    "number": 1234.56,
                    "currency": "USD",
                },
            },
            "2022-01-01 price USD" + (" " * 31) + "1234.56 USD\n",
        ),
        "document": (
            {
                "ty": "Document",
                "id": "",
                "date": "2022-01-01",
                "account": "Assets:Bank:Test",
                "filename": "test.doc",
            },
            '2022-01-01 document Assets:Bank:Test "test.doc"\n',
        ),
    }


def test_directives(client):
    expected = c.load_static_json()
    response = client.get("/directive")

    assert response.json() == expected


def test_directive(client):
    j = c.load_static_json()

    for v in DirectiveType:
        expected = jmespath.search(f"[?ty == '{v.value.capitalize()}']", j)
        response = client.get(f"/directive/{v.value}")

        assert response.json() == expected


def test_directive_id(client):
    j = c.load_static_json()

    expected = j[0]
    response = client.get(f"/directive/id/{expected['id']}")

    assert response.json() == expected


def test_directive_syntax(client, syntax: Dict[str, Tuple[Dict, str]]):
    for v in syntax.values():
        response = client.post("/directive/syntax", json=v[0])
        assert response.text == v[1]
