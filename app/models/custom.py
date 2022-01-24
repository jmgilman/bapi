import datetime

from .data import Amount
from enum import Enum
from decimal import Decimal
from pydantic import BaseModel
from typing import Union


class CustomType(str, Enum):
    amount = "amount"
    bool = "bool"
    date = "date"
    decimal = "decimal"
    str = "str"


CustomTypeMap = {
    Amount: CustomType.amount,
    bool: CustomType.bool,
    datetime.date: CustomType.date,
    Decimal: CustomType.decimal,
    str: CustomType.str,
}


class CustomEntry(BaseModel):
    type: CustomType
    value: Union[Amount, bool, Decimal, datetime.date, str]
