import pytest

from bdantic import models
from datetime import date
from .search import FullTextSearch


@pytest.fixture
def mock_transactions():
    transactions = []
    transactions.append(
        models.Transaction(
            date=date.today(),
            meta={},
            flag="*",
            payee="John",
            narration="For groceries",
            postings=[],
        )
    )
    transactions.append(
        models.Transaction(
            date=date.today(),
            meta={},
            flag="*",
            payee="Larry",
            narration="For groceries",
            postings=[],
        )
    )
    transactions.append(
        models.Transaction(
            date=date.today(),
            meta={},
            flag="*",
            payee="Outback",
            narration="Dinner",
            postings=[],
        )
    )

    return transactions


def test_index_transactions(mock_transactions):
    fts = FullTextSearch(mock_transactions)

    assert fts._transactions[0] == mock_transactions[0]
    assert fts._transactions[1] == mock_transactions[1]
    assert fts._transactions[2] == mock_transactions[2]
    assert fts._index == {
        "dinner": {2},
        "for": {0, 1},
        "groceries": {0, 1},
        "john": {0},
        "larry": {1},
        "outback": {2},
    }


def test_search(mock_transactions):
    fts = FullTextSearch(mock_transactions)

    result = fts.search("groceries")
    assert len(result) == 2
    assert mock_transactions[0] in result
    assert mock_transactions[1] in result

    result = fts.search("john groceries")
    assert len(result) == 1
    assert mock_transactions[0] == result[0]

    result = fts.search("dinner")
    assert len(result) == 1
    assert mock_transactions[2] == result[0]

    result = fts.search("john dinner")
    assert len(result) == 0


@pytest.mark.parametrize(
    "query, expected",
    [
        ("a test string", ["a", "test", "string"]),
        ("a test string.", ["a", "test", "string"]),
        ("A TEST string", ["a", "test", "string"]),
    ],
)
def test_tokenize(query, expected):
    fts = FullTextSearch([])

    tokens = fts._tokenize(query)
    assert tokens == expected
