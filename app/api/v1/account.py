from typing import Dict, List, cast

from app.api import deps
from app.core import mutate
from bdantic import models
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/",
    response_model=Dict[str, models.Account],
    summary="Fetch a list of all account names",
    response_description="A list of all account names.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def accounts(
    beanfile: models.BeancountFile = Depends(deps.get_beanfile),
) -> dict[str, models.Account]:
    return beanfile.accounts


@router.get(
    "/{account_name}",
    response_model=models.Account,
    summary="Fetch the details of an account.",
    response_description="An `Account` containing the given account details.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def account(
    acct: models.Account = Depends(deps.get_account),
) -> models.Account:
    return acct


@router.get(
    "/{account_name}/balance",
    response_model=Dict[str, models.Inventory],
    summary="Fetch the balance of an account.",
    response_description="A mapping of currencies to lists of positions.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def balance(
    acct: models.Account = Depends(deps.get_account),
) -> dict[str, models.Inventory]:
    return acct.balance


@router.get(
    "/{account_name}/transactions",
    response_model=List[models.Transaction],
    summary="Fetches all transactions associated with an account.",
    response_description="A list of transactions.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def transactions(
    acct: models.Account = Depends(deps.get_account),
    beanfile: models.BeancountFile = Depends(deps.get_beanfile),
    mutator: mutate.DirectivesMutator = Depends(deps.get_directives_mutator),
) -> list[models.Transaction]:
    txns = beanfile.entries.by_account(acct.name).by_type(models.Transaction)
    return cast(list[models.Transaction], mutator.mutate(txns).__root__)
