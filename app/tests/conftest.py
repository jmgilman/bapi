import hashlib
import json
import pickle
from datetime import date
from decimal import Decimal

import pytest
from app.api import deps
from app.api.v1 import api
from bdantic import models
from bdantic.types import ModelDirective
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(api.router)
    app.dependency_overrides[deps.get_beanfile] = _generate_beanfile

    return TestClient(app)


@pytest.fixture
def beanfile() -> models.BeancountFile:
    return _generate_beanfile()


@pytest.fixture
def entries() -> models.Directives:
    return _generate_beanfile().entries


@pytest.fixture
def raw_accounts():
    return json.loads(_generate_beanfile().json())["accounts"]


@pytest.fixture
def raw_entries():
    return json.loads(_generate_beanfile().json())["entries"]


@pytest.fixture
def raw_file():
    return json.loads(_generate_beanfile().json())


@pytest.fixture
def raw_options():
    return json.loads(_generate_beanfile().json())["options"]


@pytest.fixture
def query_response():
    return models.QueryResult(
        columns=[
            models.query.QueryColumn(name="name", type="str"),
            models.query.QueryColumn(
                name="amount",
                type="Decimal",
            ),
        ],
        rows=[{"name": "Assets:Bank:House", "amount": Decimal(800.00)}],
    )


@pytest.fixture
def syntax() -> dict[str, tuple[dict, str]]:
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


def _generate_beanfile() -> models.BeancountFile:
    dirs: list[ModelDirective] = []

    # Options
    opts = models.Options(filename="test.beancount", render_commas=False)

    # Ficticious accounts
    accounts: dict[str, models.Account] = {}
    names = [
        "Assets:Bank:House",
        "Assets:Bank:Grocery",
        "Assets:Bank:Trips",
        "Expenses:House",
        "Expenses:Grocery",
        "Expenses:Trips",
        "Assets:Bank:Closed",
    ]
    for name in names:
        dirs.append(
            models.Open(
                date=date.today(),
                meta=None,
                account=name,
                currencies=["USD", "CAD"],
            )
        )
        accounts[name] = models.Account(
            name=name,
            open=date.today(),
            balance={
                "USD": models.Inventory(
                    __root__=[
                        models.Position(
                            units=models.Amount(
                                number=Decimal(800.00), currency="USD"
                            )
                        )
                    ]
                )
            },
        )

    # Close out an account
    dirs.append(
        models.Close(
            date=date.today(),
            meta=None,
            account="Assets:Bank:Closed",
        )
    )

    # Commodities
    dirs.append(models.Commodity(date=date.today(), meta=None, currency="USD"))
    dirs.append(models.Commodity(date=date.today(), meta=None, currency="CAD"))

    # Some transactions
    dirs.append(
        models.Transaction(
            date=date.today(),
            meta=None,
            flag="*",
            payee="Home Depot",
            narration="Bought some things",
            links={"link1"},
            tags={"tag1"},
            postings=[
                models.Posting(
                    account=names[0],
                    units=models.Amount(number=Decimal(-19.99)),
                ),
                models.Posting(
                    account=names[3],
                    units=models.Amount(number=Decimal(19.99)),
                ),
            ],
        )
    )
    dirs.append(
        models.Transaction(
            date=date.today(),
            meta=None,
            flag="*",
            payee="Safeway",
            narration="Milk",
            links={"link1"},
            tags={"tag1"},
            postings=[
                models.Posting(
                    account=names[1],
                    units=models.Amount(number=Decimal(-2.99)),
                ),
                models.Posting(
                    account=names[4],
                    units=models.Amount(number=Decimal(2.99)),
                ),
            ],
        )
    )
    dirs.append(
        models.Transaction(
            date=date.today(),
            meta=None,
            flag="*",
            payee="Disneyland",
            narration="Admission",
            links={"link1"},
            tags={"tag1"},
            postings=[
                models.Posting(
                    account=names[2],
                    units=models.Amount(number=Decimal(-499.99)),
                ),
                models.Posting(
                    account=names[5],
                    units=models.Amount(number=Decimal(499.99)),
                ),
            ],
        )
    )

    # All other directives
    dirs.append(
        models.Document(
            date=date.today(),
            meta=None,
            account=names[0],
            filename="test/file.jpg",
            tags={"tag1"},
            links={"link1"},
        )
    )
    dirs.append(
        models.Event(
            date=date.today(),
            meta=None,
            type="test",
            description="some kind of event",
        )
    )
    dirs.append(
        models.Note(
            date=date.today(),
            meta=None,
            account=names[0],
            comment="A test comment",
        )
    )
    dirs.append(
        models.Pad(
            date=date.today(),
            meta=None,
            account=names[0],
            source_account=names[1],
        )
    )
    dirs.append(
        models.Price(
            date=date.today(),
            meta=None,
            currency="EUR",
            amount=models.Amount(number=None, currency=None),
        )
    )
    dirs.append(
        models.Query(
            date=date.today(),
            meta=None,
            name="Test query",
            query_string="SELECT *",
        )
    )

    # Generate ID's
    for d in dirs:
        d.id = hashlib.md5(pickle.dumps(d)).hexdigest()

    return models.BeancountFile(
        entries=models.Directives(__root__=dirs),
        options=opts,
        errors=[],
        accounts=accounts,
    )
