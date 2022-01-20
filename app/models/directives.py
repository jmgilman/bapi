import datetime
from hashlib import new
import itertools

from beancount.core import data
from .data import Account, Amount, Booking, Currency, Flag, Posting
from .data import to_model as to_data_model
from .data import from_model as from_data_model
from decimal import Decimal
from fastapi import encoders
from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Set, Union


class BaseDirective(BaseModel):
    """Contains common attributes on all directives."""

    date: datetime.date
    meta: Dict[str, Any]


class Open(BaseDirective):
    account: Account
    currencies: Optional[List[Currency]]
    booking: Optional[Booking]


class Close(BaseDirective):
    account: Account


class Commodity(BaseDirective):
    currency: Currency


class Pad(BaseDirective):
    account: Account
    source_account: Account


class Balance(BaseDirective):
    account: Account
    amount: Amount
    tolerance: Optional[float]
    diff_amount: Optional[Amount]


class Transaction(BaseDirective):
    flag: Flag
    payee: Optional[str]
    narration: str
    tags: Optional[Set]
    links: Optional[Set]
    postings: List[Posting]


class TxnPosting(BaseDirective):
    txn: Transaction
    posting: Posting


class Note(BaseDirective):
    account: Account
    comment: str


class Event(BaseDirective):
    type: str
    description: str


class Query(BaseDirective):
    name: str
    query_string: str


class Price(BaseDirective):
    currency: Currency
    amount: Amount


class Document(BaseDirective):
    account: Account
    filename: str
    tags: Optional[Set]
    links: Optional[Set]


class Custom(BaseDirective):
    type: str
    values: List[Any]


Directive = Union[
    Open,
    Close,
    Commodity,
    Pad,
    Balance,
    Transaction,
    Note,
    Event,
    Query,
    Price,
    Document,
    Custom,
]


class Directives(BaseModel):
    open: List[Open] = []
    close: List[Close] = []
    commodity: List[Commodity] = []
    pad: List[Pad] = []
    balance: List[Balance] = []
    transaction: List[Transaction] = []
    note: List[Note] = []
    event: List[Event] = []
    query: List[Query] = []
    price: List[Price] = []
    document: List[Document] = []
    custom: List[Custom] = []

    def __init__(self, directives: List[Directive]):
        super().__init__()
        for directive in directives:
            if isinstance(directive, Open):
                self.open.append(directive)
            elif isinstance(directive, Close):
                self.close.append(directive)
            elif isinstance(directive, Commodity):
                self.commodity.append(directive)
            elif isinstance(directive, Pad):
                self.pad.append(directive)
            elif isinstance(directive, Balance):
                self.balance.append(directive)
            elif isinstance(directive, Transaction):
                self.transaction.append(directive)
            elif isinstance(directive, Note):
                self.note.append(directive)
            elif isinstance(directive, Event):
                self.event.append(directive)
            elif isinstance(directive, Query):
                self.query.append(directive)
            elif isinstance(directive, Price):
                self.price.append(directive)
            elif isinstance(directive, Document):
                self.document.append(directive)
            elif isinstance(directive, Custom):
                self.custom.append(directive)

    def all(self) -> List[Directive]:
        """Returns a list of all directives held by this instance."""
        return list(itertools.chain(*self.__dict__.values()))


class DirectiveNotFound(Exception):
    """Thrown when a matching model is not found for the given directive."""

    pass


def to_model(directive: data.Directive) -> Directive:
    """Converts a beancount core directive into its pydantic equivalent.

    Args:
        directive: The beancount directive to convert.

    Raises:
        DirectiveNotFound: No equivalent pydantic model was found.
    """
    if isinstance(directive, data.Open):
        return Open(
            date=directive.date,
            meta=filter_meta(directive.meta),
            account=directive.account,
            currencies=directive.currencies,
            booking=directive.booking,
        )
    elif isinstance(directive, data.Close):
        return Close(
            date=directive.date,
            meta=filter_meta(directive.meta),
            account=directive.account,
        )
    elif isinstance(directive, data.Commodity):
        return Commodity(
            date=directive.date, meta=directive.meta, currency=directive.currency
        )
    elif isinstance(directive, data.Pad):
        return Pad(
            date=directive.date,
            meta=filter_meta(directive.meta),
            account=directive.account,
            source_account=directive.source_account,
        )
    elif isinstance(directive, data.Balance):
        return Balance(
            date=directive.date,
            meta=filter_meta(directive.meta),
            account=directive.account,
            amount=to_data_model(directive.amount),
            tolerance=float(directive.tolerance) if directive.tolerance else None,
            diff_amount=to_data_model(directive.diff_amount),
        )
    elif isinstance(directive, data.Transaction):
        return Transaction(
            date=directive.date,
            meta=filter_meta(directive.meta),
            flag=directive.flag,
            payee=directive.payee,
            narration=directive.narration,
            tags=directive.tags,
            links=directive.links,
            postings=[to_data_model(posting) for posting in directive.postings],
        )
    elif isinstance(directive, data.Note):
        return Note(
            date=directive.date,
            meta=filter_meta(directive.meta),
            account=directive.account,
            comment=directive.comment,
        )
    elif isinstance(directive, data.Event):
        return Event(
            date=directive.date,
            meta=filter_meta(directive.meta),
            type=directive.type,
            description=directive.description,
        )
    elif isinstance(directive, data.Query):
        return Query(
            date=directive.date,
            meta=filter_meta(directive.meta),
            name=directive.name,
            query_string=directive.query_string,
        )
    elif isinstance(directive, data.Price):
        return Price(
            date=directive.date,
            meta=filter_meta(directive.meta),
            currency=directive.currency,
            amount=to_data_model(directive.amount),
        )
    elif isinstance(directive, data.Document):
        return Document(
            date=directive.date,
            meta=filter_meta(directive.meta),
            account=directive.account,
            filename=directive.filename,
            tags=directive.tags,
            links=directive.links,
        )
    elif isinstance(directive, data.Custom):
        return Custom(
            date=directive.date,
            meta=filter_meta(directive.meta),
            type=directive.type,
            values=directive.values,
        )
    elif directive is None:
        return None
    else:
        raise DirectiveNotFound


def from_model(directive: Directive) -> data.Directive:
    """Converts a pydyantic directive into its beancount equivalent.

    Args:
        directive: The directive to convert.

    Raises:
        DirectiveNotFound: No equivalent beancount model was found.
    """
    if isinstance(directive, Open):
        return data.Open(
            date=directive.date,
            meta=directive.meta,
            account=directive.account,
            currencies=directive.currencies,
            booking=directive.booking,
        )
    elif isinstance(directive, Close):
        return data.Close(
            date=directive.date,
            meta=directive.meta,
            account=directive.account,
        )
    elif isinstance(directive, Commodity):
        return data.Commodity(
            date=directive.date, meta=directive.meta, currency=directive.currency
        )
    elif isinstance(directive, Pad):
        return data.Pad(
            date=directive.date,
            meta=directive.meta,
            account=directive.account,
            source_account=directive.source_account,
        )
    elif isinstance(directive, Balance):
        return data.Balance(
            date=directive.date,
            meta=directive.meta,
            account=directive.account,
            amount=from_data_model(directive.amount),
            tolerance=Decimal(directive.tolerance),
            diff_amount=from_data_model(directive.diff_amount),
        )
    elif isinstance(directive, Transaction):
        return data.Transaction(
            date=directive.date,
            meta=directive.meta,
            flag=directive.flag,
            payee=directive.payee,
            narration=directive.narration,
            tags=directive.tags,
            links=directive.links,
            postings=[from_data_model(posting) for posting in directive.postings],
        )
    elif isinstance(directive, Note):
        return data.Note(
            date=directive.date,
            meta=directive.meta,
            account=directive.account,
            comment=directive.comment,
        )
    elif isinstance(directive, Event):
        return data.Event(
            date=directive.date,
            meta=directive.meta,
            type=directive.type,
            description=directive.description,
        )
    elif isinstance(directive, Query):
        return data.Query(
            date=directive.date,
            meta=directive.meta,
            name=directive.name,
            query_string=directive.query_string,
        )
    elif isinstance(directive, Price):
        return data.Price(
            date=directive.date,
            meta=directive.meta,
            currency=directive.currency,
            amount=from_data_model(directive.amount),
        )
    elif isinstance(directive, Document):
        return data.Document(
            date=directive.date,
            meta=directive.meta,
            account=directive.account,
            filename=directive.filename,
            tags=directive.tags,
            links=directive.links,
        )
    elif isinstance(directive, Custom):
        return data.Custom(
            date=directive.date,
            meta=directive.meta,
            type=directive.type,
            values=directive.values,
        )
    elif directive is None:
        return None
    else:
        raise DirectiveNotFound


def filter_meta(meta: Dict[str, Any]) -> Dict[str, Any]:
    new_meta = {}
    for key, value in meta.items():
        try:
            encoders.jsonable_encoder(value)
        except:
            continue
        new_meta[key] = value

    return new_meta
