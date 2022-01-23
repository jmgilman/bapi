import inspect
import pytest

from beancount.core.data import Amount, Cost, CostSpec, Posting
from datetime import date

from .data import from_model, to_model, DataNotFound
from decimal import Decimal


@pytest.fixture
def mock_data():
    data = []
    data.append(Amount(number=Decimal(1234.00), currency="USD"))
    data.append(
        Cost(
            number=Decimal(1234.00),
            currency="USD",
            date=date.today(),
            label="test",
        )
    )
    data.append(
        CostSpec(
            number_per=Decimal(1234.00),
            number_total=Decimal(4321.00),
            currency="USD",
            date=date.today(),
            label="test",
            merge=True,
        )
    )
    data.append(
        Posting(
            account="Assets:Bank",
            units=Amount(number=Decimal(1234), currency="USD"),
            cost=None,
            price=None,
            flag=None,
            meta={},
        )
    )

    return data


def assert_is_equal(object1, object2):
    for attribute in object1:
        if not attribute[0].startswith("__") and not inspect.ismethod(
            attribute[1]
        ):
            assert object2.__getattribute__(attribute[0]) == attribute[1]


def test_to_from_model(mock_data):
    for data in mock_data:
        model = to_model(data)
        assert_is_equal(model, data)
        model = from_model(model)
        assert model == data

    with pytest.raises(DataNotFound):
        model = to_model(mock_data[0])
        to_model(model)

    with pytest.raises(DataNotFound):
        from_model(mock_data[0])
