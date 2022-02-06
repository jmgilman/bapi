from beancount.core import data
from bdantic.models.file import Directives
from bdantic.types import ModelDirective
from ..dependencies import (
    get_beanfile,
    get_directives,
    get_filter,
)
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from ..internal.beancount import BeancountFile
from typing import List

router = APIRouter(prefix="/directive", tags=["directives"])


@router.get(
    "/",
    response_model=Directives,
    summary="Fetches all directives in the beancount ledger.",
    response_description="A list of all directives.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
def directives(
    beanfile: BeancountFile = Depends(get_beanfile), filter=Depends(get_filter)
):
    return filter(Directives.parse(beanfile.entries))


@router.get(
    "/{directive}",
    response_model=Directives,
    summary="Fetches all directives of the requested type.",
    response_description="A list of all directives of the requested type.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
def directive(
    directives: List[data.Directive] = Depends(get_directives),
    filter=Depends(get_filter),
):
    return filter(directives)


@router.post(
    "/syntax",
    response_class=PlainTextResponse,
    summary="Generate syntax for the given directive",
    response_description="The Beancount syntax for the given directive",
)
def directive_syntax(
    data: ModelDirective,
):
    return data.syntax()
