from bdantic import models
from bdantic.types import ModelDirective
from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse

from app.api import deps
from app.core import mutate

router = APIRouter()


@router.get(
    "/",
    response_model=models.Directives,
    summary="Fetches all directives in the beancount ledger.",
    response_description="A list of all directives.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def directives(
    beanfile: models.BeancountFile = Depends(deps.get_beanfile),
    mutator: mutate.DirectivesMutator = Depends(deps.get_directives_mutator),
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
    beanfile: models.BeancountFile = Depends(deps.get_beanfile),
    directive: deps.DirectiveType = Path(
        "", description="The type of directive to fetch"
    ),
    mutator: mutate.DirectivesMutator = Depends(deps.get_directives_mutator),
):
    typ = deps.get_directive_type(directive)
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
    beanfile: models.BeancountFile = Depends(deps.get_beanfile),
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
