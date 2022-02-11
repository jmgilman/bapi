import pytest

from . import mutate
from bdantic import models
from datetime import date
from decimal import Decimal


@pytest.fixture
def data():
    dirs = []
    dirs.append(models.Open(date=date.today(), account="Assets:Test"))
    dirs.append(models.Open(date=date.today(), account="Assets:Testing"))
    dirs.append(models.Open(date=date.today(), account="Expenses:Test"))
    dirs.append(
        models.Pad(
            date=date.today(),
            account="Assets:Testing",
            source_account="Assets:Test",
        )
    )
    dirs.append(
        models.Transaction(
            date=date.today(),
            flag="*",
            payee="Home Depot",
            narration="Tools",
            postings=[
                models.Posting(
                    account="Assets:Test",
                    units=models.Amount(number=Decimal(-1.50), currency="USD"),
                ),
                models.Posting(
                    account="Expenses:Test",
                    units=models.Amount(number=Decimal(1.50), currency="USD"),
                ),
            ],
        )
    )

    return models.Directives(__root__=dirs)


def test_directives(data):
    mut = mutate.DirectivesMutator()
    result = mut.mutate(data)
    assert result == data

    mut = mutate.DirectivesMutator(filter_expr="[?ty == 'Open']")
    result = mut.mutate(data)
    assert result == models.Directives(__root__=data[:3])

    mut = mutate.DirectivesMutator(search_expr="Home Depot")
    result = mut.mutate(data)
    assert result == models.Directives(__root__=[data[4]])
