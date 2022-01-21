import inspect
import pytest

from beancount.core.data import (
    Open,
    Close,
    Commodity,
    Pad,
    Balance,
    Transaction,
    TxnPosting,
    Note,
    Event,
    Query,
    Price,
    Document,
    Custom,
    Amount,
    Posting,
)
from datetime import date
from decimal import Decimal
from .directives import from_model, to_model, DirectiveNotFound


@pytest.fixture
def mock_directives():
    postings = [
        Posting(
            account="Assets:Bank:Groceries",
            units=Amount(Decimal(-1234.00), currency="USD"),
            cost=None,
            price=None,
            flag=None,
            meta={},
        ),
        Posting(
            account="Expenses:Groceries",
            units=Amount(Decimal(1234.00), currency="USD"),
            cost=None,
            price=None,
            flag=None,
            meta={},
        ),
    ]
    txn = Transaction(
        date=date.today(),
        meta={},
        flag="*",
        payee="John",
        narration="For groceries",
        tags=None,
        links=None,
        postings=postings,
    )

    directives = []
    directives.append(
        Open(
            date=date.today(),
            meta={},
            account="Assets:Bank",
            currencies=None,
            booking=None,
        )
    )
    directives.append(Close(date=date.today(), meta={}, account="Assets:Bank"))
    directives.append(Commodity(date=date.today(), meta={}, currency="USD"))
    directives.append(
        Pad(
            date=date.today(),
            meta={},
            account="Assets:Bank",
            source_account="Assets:Savings",
        )
    )
    directives.append(
        Balance(
            date=date.today(),
            meta={},
            account="Assets:Bank",
            amount=Amount(Decimal(1234.00), currency="USD"),
            tolerance=None,
            diff_amount=None,
        )
    )
    directives.append(txn)
    directives.append(TxnPosting(txn=txn, posting=postings[0]))
    directives.append(
        Note(
            date=date.today(),
            meta={},
            account="Assets:Bank",
            comment="Test comment",
        )
    )
    directives.append(
        Event(
            date=date.today(),
            meta={},
            type="Test type",
            description="Test description",
        )
    )
    directives.append(
        Query(
            date=date.today(),
            meta={},
            name="test",
            query_string="query string",
        )
    )
    directives.append(
        Price(
            date=date.today(),
            meta={},
            currency="USD",
            amount=Amount(Decimal(1234.00), "USD"),
        )
    )
    directives.append(
        Document(
            date=date.today(),
            meta={},
            account="Assets:Bank",
            filename="file.beancount",
            tags=None,
            links=None,
        )
    )
    directives.append(
        Custom(
            date=date.today(),
            meta={},
            type="custom",
            values=[],
        )
    )

    return directives


def assert_is_equal(object1, object2):
    for attribute in object1:
        if not attribute[0].startswith("__") and not inspect.ismethod(attribute[1]):
            attribute1 = attribute[1]
            attribute2 = object2.__getattribute__(attribute[0])

            if isinstance(attribute1, list):
                for sub_attribute1, sub_attribute2 in zip(attribute1, attribute2):
                    return assert_is_equal(sub_attribute1, sub_attribute2)

            if (
                isinstance(attribute2, Amount)
                or isinstance(attribute2, Posting)
                or isinstance(attribute2, Transaction)
            ):
                return assert_is_equal(attribute1, attribute2)

            assert attribute1 == attribute2


def test_to_from_model(mock_directives):
    for directive in mock_directives:
        model = to_model(directive)
        assert_is_equal(model, directive)
        model = from_model(model)
        assert model == directive

    with pytest.raises(DirectiveNotFound):
        model = to_model(mock_directives[0])
        to_model(model)

    with pytest.raises(DirectiveNotFound):
        from_model(mock_directives[0])
