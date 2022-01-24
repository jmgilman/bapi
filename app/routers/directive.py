import datetime

from beancount.parser import printer
from beancount.core.amount import Amount
from dateutil import parser
from decimal import Decimal, getcontext
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from ..dependencies import get_beanfile
from ..models.custom import CustomType
from ..models.directives import (
    from_model,
    Directive,
    Balance,
    Close,
    Commodity,
    Custom,
    Document,
    Event,
    Note,
    Open,
    Pad,
    Price,
    Query,
    Transaction,
)
from typing import List

router = APIRouter(prefix="/directive", tags=["directives"])


@router.get(
    "/",
    response_model=List[Directive],
    summary="Fetches all directives in the beancount ledger.",
    response_description="A list of all directives.",
)
def directive(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.all()


@router.get(
    "/open",
    response_model=List[Directive],
    summary="Fetches all open directives in the beancount ledger.",
    response_description="A list of all open directives.",
)
def directive_open(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.open


@router.post(
    "/open",
    response_class=PlainTextResponse,
    summary="Generate syntax for an Open directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_open_generate(open: Open):
    open = from_model(open)
    return printer.format_entry(open)


@router.get(
    "/close",
    response_model=List[Directive],
    summary="Fetches all close directives in the beancount ledger.",
    response_description="A list of all close directives.",
)
def directive_close(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.close


@router.post(
    "/close",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Close directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_close_generate(close: Close):
    close = from_model(close)
    return printer.format_entry(close)


@router.get(
    "/commodity",
    response_model=List[Directive],
    summary="Fetches all commodity directives in the beancount ledger.",
    response_description="A list of all commodity directives.",
)
def directive_commodity(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.commodity


@router.post(
    "/commodity",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Commodity directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_commodity_generate(commodity: Commodity):
    commodity = from_model(commodity)
    return printer.format_entry(commodity)


@router.get(
    "/pad",
    response_model=List[Directive],
    summary="Fetches all pad directives in the beancount ledger.",
    response_description="A list of all pad directives.",
)
def directive_pad(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.pad


@router.post(
    "/pad",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Pad directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_pad_generate(pad: Pad):
    pad = from_model(pad)
    return printer.format_entry(pad)


@router.get(
    "/balance",
    response_model=List[Directive],
    summary="Fetches all balance directives in the beancount ledger.",
    response_description="A list of all balance directives.",
)
def directive_balance(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.balance


@router.post(
    "/balance",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Balance directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_balance_generate(balance: Balance):
    balance = from_model(balance)
    return printer.format_entry(balance)


@router.get(
    "/transaction",
    response_model=List[Directive],
    summary="Fetches all transaction directives in the beancount ledger.",
    response_description="A list of all transaction directives.",
)
def directive_transaction(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.transaction


@router.post(
    "/transaction",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Transaction directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_transaction_generate(transaction: Transaction):
    transaction = from_model(transaction)
    return printer.format_entry(transaction)


@router.get(
    "/note",
    response_model=List[Directive],
    summary="Fetches all note directives in the beancount ledger.",
    response_description="A list of all note directives.",
)
def directive_note(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.note


@router.post(
    "/note",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Note directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_note_generate(note: Note):
    note = from_model(note)
    return printer.format_entry(note)


@router.get(
    "/event",
    response_model=List[Directive],
    summary="Fetches all event directives in the beancount ledger.",
    response_description="A list of all event directives.",
)
def directive_event(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.event


@router.post(
    "/event",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Event directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_event_generate(event: Event):
    event = from_model(event)
    return printer.format_entry(event)


@router.get(
    "/query",
    response_model=List[Directive],
    summary="Fetches all query directives in the beancount ledger.",
    response_description="A list of all query directives.",
)
def directive_query(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.query


@router.post(
    "/query",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Query directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_query_generate(query: Query):
    query = from_model(query)
    return printer.format_entry(query)


@router.get(
    "/price",
    response_model=List[Directive],
    summary="Fetches all price directives in the beancount ledger.",
    response_description="A list of all price directives.",
)
def directive_price(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.price


@router.post(
    "/price",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Price directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_price_generate(price: Price):
    price = from_model(price)
    return printer.format_entry(price)


@router.get(
    "/document",
    response_model=List[Directive],
    summary="Fetches all document directives in the beancount ledger.",
    response_description="A list of all document directives.",
)
def directive_document(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.document


@router.post(
    "/document",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Document directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_document_generate(document: Document):
    document = from_model(document)
    return printer.format_entry(document)


@router.get(
    "/custom",
    response_model=List[Directive],
    summary="Fetches all custom directives in the beancount ledger.",
    response_description="A list of all custom directives.",
)
def directive_custom(
    beanfile=Depends(get_beanfile),
):
    return beanfile.directives.custom


@router.post(
    "/custom",
    response_class=PlainTextResponse,
    summary="Generate syntax for a Custom directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_custom_generate(custom: Custom):
    custom = from_model(custom)
    for i, (value, type) in enumerate(custom.values):
        if type == CustomType.amount:
            custom.values[i] = (
                Amount(
                    number=Decimal(value["number"]),
                    currency=str(value["currency"]),
                ),
                Amount,
            )
        elif type == CustomType.bool:
            custom.values[i] = (bool(value), bool)
        elif type == CustomType.date:
            custom.values[i] = (parser.parse(value).date(), datetime.date)
        elif type == CustomType.decimal:
            getcontext().prec = 2
            custom.values[i] == (Decimal(value), Decimal)
        elif type == CustomType.str:
            custom.values[i] == (str(value), str)

    return printer.format_entry(custom)
