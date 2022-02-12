from typing import List

from app.api import deps
from bdantic import models
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/",
    response_model=models.BeancountFile,
    summary="Fetches the entire contents of the beancount ledger.",
    response_description="A BeancountFile containing contents of the ledger.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def file(
    beanfile: models.BeancountFile = Depends(deps.get_beanfile),
) -> models.BeancountFile:
    return beanfile


@router.get(
    "/errors",
    response_model=List[str],
    summary="Fetches the errors generated from parsing the ledger.",
    response_description="A list of errors generated from parsing the ledger.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def errors(
    beanfile: models.BeancountFile = Depends(deps.get_beanfile),
) -> list:
    return beanfile.errors


@router.get(
    "/options",
    response_model=models.file.Options,
    summary="Fetches the options from the beancount ledger.",
    response_description="An Options containing the ledger options.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def options(
    beanfile: models.BeancountFile = Depends(deps.get_beanfile),
) -> models.file.Options:
    return beanfile.options
