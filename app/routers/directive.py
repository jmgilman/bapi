from bdantic import models
from bdantic.types import ModelDirective
from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse

from .. import dependencies as dep
from .. import models as mod

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
    mutator: dep.DirectivesMutator = Depends(dep.get_directives_mutator),
):
    return mutator.mutate(beanfile.entries)


@router.get(
    "/{directive}",
    response_model=models.Directives,
    summary="Fetches all directives of the requested type.",
    response_description="A list of all directives of the requested type.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def directive(
    beanfile: models.BeancountFile = Depends(dep.get_beanfile),
    directive: mod.DirectiveType = Path(
        "", description="The type of directive to fetch"
    ),
    mutator: dep.DirectivesMutator = Depends(dep.get_directives_mutator),
):
    typ = mod.get_directive_type(directive)
    directives = beanfile.entries.by_type(typ)  # type: ignore
    return mutator.mutate(directives)


@router.get(
    "/id/{id}",
    response_model=ModelDirective,  # type: ignore
    summary="Fetches a directive by ID.",
    response_description="The associated directive.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def directive_id(
    id: str = Path("", description="The ID of the directive to fetch."),
    beanfile: models.BeancountFile = Depends(dep.get_beanfile),
) -> ModelDirective:
    try:
        return beanfile.entries.by_id(id)
    except models.file.IDNotFoundError:
        raise HTTPException(status_code=404, detail="Directive not found")


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
