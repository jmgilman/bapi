from fastapi import APIRouter, Depends
from ..dependencies import get_beanfile
from ..models.directives import Directive
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
