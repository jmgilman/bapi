from .. import dependencies as dep
from beancount.core import data
from bdantic.models.file import Directives
from bdantic.types import ModelDirective
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
    beanfile: BeancountFile = Depends(dep.get_beanfile),
    filter=Depends(dep.get_filter),
    search=Depends(dep.get_search_directives),
    priority=Depends(dep.get_mutate_priority),
):
    if priority == dep.MutatePriority.filter:
        return search(filter(Directives.parse(beanfile.entries)))
    else:
        return filter(search(Directives.parse(beanfile.entries)))


@router.get(
    "/{directive}",
    response_model=Directives,
    summary="Fetches all directives of the requested type.",
    response_description="A list of all directives of the requested type.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
def directive(
    directives: List[data.Directive] = Depends(dep.get_directives),
    filter=Depends(dep.get_filter),
    search=Depends(dep.get_search_directives),
    priority=Depends(dep.get_mutate_priority),
):
    if priority == dep.MutatePriority.filter:
        return search(filter(directives))
    else:
        return filter(search(directives))


@router.post(
    "/syntax",
    response_class=PlainTextResponse,
    summary="Generate syntax for the given directive.",
    response_description="The Beancount syntax for the given directive.",
)
def directive_syntax(
    data: ModelDirective,
):
    return data.syntax()
