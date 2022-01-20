import datetime

from beancount.core import data
from decimal import Decimal
from pydantic import BaseModel
from typing import Any, Dict, Optional, Union

Account = str
Booking = data.Booking
Currency = str
Flag = str
Meta = Dict[str, Any]


class Amount(BaseModel):
    number: Optional[float]
    currency: str


class Cost(BaseModel):
    number: float
    currency: str
    date: datetime.date
    label: Optional[str]


class CostSpec(BaseModel):
    number_per: Optional[float]
    number_total: Optional[float]
    currency: Optional[str]
    date: Optional[datetime.date]
    label: Optional[str]
    merge: Optional[bool]


class Posting(BaseModel):
    account: str
    units: Amount
    cost: Optional[Union[Cost, CostSpec]]
    price: Optional[Amount]
    flag: Optional[str]
    meta: Optional[Dict[str, Any]]


class DataNotFound(Exception):
    """Thrown when a matching model is not found for the given data object."""

    pass


Data = Union[Amount, Cost, CostSpec, Posting]


def to_model(
    object: Union[data.Amount, data.Cost, data.CostSpec, data.Posting]
) -> Data:
    """Converts a beancount core data type into its pydantic equivalent.

    Args:
        data: The beancount data type to convert.

    Raises:
        DataNotFound: No equivalent pydantic model was found.
    """
    if isinstance(object, data.Amount):
        return Amount(number=object.number, currency=object.currency)
    elif isinstance(object, data.Cost):
        return Cost(
            number=float(object.number),
            currency=object.currency,
            date=object.date,
            label=object.label,
        )
    elif isinstance(object, data.CostSpec):
        return CostSpec(
            number_per=float(object.number_per),
            number_total=float(object.number_total),
            currency=object.currency,
            date=object.date,
            label=object.label,
            merge=object.merge,
        )
    elif isinstance(object, data.Posting):
        return Posting(
            account=object.account,
            units=to_model(object.units),
            cost=to_model(object.cost),
            price=to_model(object.price),
            flag=object.flag,
            meta=object.meta,
        )
    elif object is None:
        return None
    else:
        raise DataNotFound


def from_model(
    object: Union[data.Amount, data.Cost, data.CostSpec, data.Posting]
) -> Data:
    """Converts a pydantic core data type into its beancount equivalent.

    Args:
        data: The data type to convert.

    Raises:
        DataNotFound: No equivalent beancount model was found.
    """
    if isinstance(object, Amount):
        return data.Amount(number=object.number, currency=object.currency)
    elif isinstance(object, Cost):
        return data.Cost(
            number=Decimal(object.number),
            currency=object.currency,
            date=object.date,
            label=object.label,
        )
    elif isinstance(object, CostSpec):
        return data.CostSpec(
            number_per=Decimal(object.number_per),
            number_total=Decimal(object.number_total),
            currency=object.currency,
            date=object.date,
            label=object.label,
            merge=object.merge,
        )
    elif isinstance(object, Posting):
        return data.Posting(
            account=object.account,
            units=from_model(object.units),
            cost=from_model(object.cost),
            price=from_model(object.price),
            flag=object.flag,
            meta=object.meta,
        )
    elif object is None:
        return None
    else:
        raise DataNotFound
