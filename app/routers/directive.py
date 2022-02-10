from .. import dependencies as dep
from bdantic import models
from bdantic.types import ModelDirective
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/directive", tags=["directives"])


@router.get(
    "/",
    response_model=models.Directives,
    summary="Fetches all directives in the beancount ledger.",
    response_description="A list of all directives.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def directives(
    beanfile: models.BeancountFile = Depends(dep.get_beanfile),
    filter=Depends(dep.get_filter),
    search=Depends(dep.get_search_directives),
    priority=Depends(dep.get_mutate_priority),
):
    if priority == dep.MutatePriority.filter:
        return search(filter(beanfile.entries))
    else:
        return filter(search(beanfile.entries))


@router.get(
    "/{directive}",
    response_model=models.Directives,
    summary="Fetches all directives of the requested type.",
    response_description="A list of all directives of the requested type.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def directive(
    directives: models.Directives = Depends(dep.get_directives),
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
async def directive_syntax(
    data: ModelDirective,
):
    return data.syntax()
