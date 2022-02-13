from datetime import date

import pytest
from bdantic import models

from app.core import search


def test_index_entry():
    fts = search.FullTextSearch([])
    fts._index_entry(1, "some words", "data")

    assert fts._entries[1] == "data"
    assert fts._index["some"] == {1}
    assert fts._index["words"] == {1}


def test_search():
    index = [
        ("some words", "data1"),
        ("more words", "data2"),
        ("something else", "data3"),
    ]
    fts = search.FullTextSearch(index)

    expected = ["data1", "data2"]
    assert fts.search("words") == expected

    expected = ["data1"]
    assert fts.search("some") == expected

    expected = ["data2"]
    assert fts.search("more words") == expected

    expected = ["data3"]
    assert fts.search("something else")


@pytest.mark.parametrize(
    "query, expected",
    [
        ("a test string", ["a", "test", "string"]),
        ("a test string.", ["a", "test", "string"]),
        ("A TEST string", ["a", "test", "string"]),
    ],
)
def test_tokenize(query, expected):
    fts = search.FullTextSearch([])

    tokens = fts._tokenize(query)
    assert tokens == expected


def test_search_directives():
    e = models.Directives(__root__=[])

    # Close
    d = models.Directives(
        __root__=[
            models.Close(
                id="",
                date=date.today(),
                meta=None,
                account="Assets:Test",
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("Assets:Test") == d
    assert fts.search("Assets") == e

    # Commodity
    d = models.Directives(
        __root__=[
            models.Commodity(
                id="", date=date.today(), meta=None, currency="USD"
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("USD") == d
    assert fts.search("CAD") == e

    # Document
    d = models.Directives(
        __root__=[
            models.Document(
                id="",
                date=date.today(),
                meta=None,
                account="Assets:Test",
                filename="test/file.jpg",
                tags={"tag1"},
                links={"link1"},
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("Assets:Test") == d
    assert fts.search("file.jpg") == d
    assert fts.search("tag1") == d
    assert fts.search("link1") == d
    assert fts.search("link") == e

    # Event
    d = models.Directives(
        __root__=[
            models.Event(
                id="",
                date=date.today(),
                meta=None,
                type="test",
                description="some kind of event",
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("test") == d
    assert fts.search("some kind") == d
    assert fts.search("events") == e

    # Note
    d = models.Directives(
        __root__=[
            models.Note(
                id="",
                date=date.today(),
                meta=None,
                account="Assets:Test",
                comment="A test comment",
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("Assets:Test") == d
    assert fts.search("a test") == d
    assert fts.search("comments") == e

    # Open
    d = models.Directives(
        __root__=[
            models.Open(
                id="",
                date=date.today(),
                meta=None,
                account="Assets:Test",
                currencies=["USD", "CAD"],
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("Assets:Test") == d
    assert fts.search("USD") == d
    assert fts.search("EUR") == e

    # Pad
    d = models.Directives(
        __root__=[
            models.Pad(
                id="",
                date=date.today(),
                meta=None,
                account="Assets:Test",
                source_account="Assets:Test1",
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("Assets:Test") == d
    assert fts.search("Assets:Test1") == d
    assert fts.search("Assets") == e

    # Price
    d = models.Directives(
        __root__=[
            models.Price(
                id="",
                date=date.today(),
                meta=None,
                currency="USD",
                amount=models.Amount(number=None, currency=None),
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("USD") == d
    assert fts.search("EUR") == e

    # Query
    d = models.Directives(
        __root__=[
            models.Query(
                id="",
                date=date.today(),
                meta=None,
                name="Test query",
                query_string="SELECT *",
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("query") == d
    assert fts.search("SELECT") == d
    assert fts.search("queries") == e

    # Transaction
    d = models.Directives(
        __root__=[
            models.Transaction(
                id="",
                date=date.today(),
                meta=None,
                flag="*",
                payee="The Store",
                narration="Bought some things",
                links={"link1"},
                tags={"tag1"},
                postings=[],
            )
        ]
    )
    fts = search.DirectiveSearcher(d)
    assert fts.search("store") == d
    assert fts.search("things") == d
    assert fts.search("link1") == d
    assert fts.search("tag1") == d
    assert fts.search("Bought some more things") == e
