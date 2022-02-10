from .. import dependencies as dep
from bdantic import models
from fastapi import APIRouter, Depends
from typing import Dict, List

router = APIRouter(prefix="/account", tags=["accounts"])


@router.get(
    "/",
    response_model=List[str],
    summary="Fetch a list of all account names",
    response_description="A list of all account names.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def accounts(
    beanfile: models.BeancountFile = Depends(dep.get_beanfile),
    search=Depends(dep.get_search_accounts),
) -> List[str]:
    return search(list(beanfile.accounts.keys()))


@router.get(
    "/{account_name}",
    response_model=models.Account,
    summary="Fetch the details of an account.",
    response_description="An `Account` containing the given account details.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def account(
    acct: models.Account = Depends(dep.get_account),
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
    acct: models.Account = Depends(dep.get_account),
) -> Dict[str, models.Inventory]:
    return acct.balance


@router.get(
    "/{account_name}/realize",
    response_model=models.RealAccount,
    summary="Fetch the result of realizing an account.",
    response_description="The raw results from calling realization.realize().",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def realize(
    real_acct: models.RealAccount = Depends(dep.get_real_account),
) -> models.RealAccount:
    return real_acct


@router.get(
    "/{account_name}/transactions",
    response_model=List[models.Transaction],
    summary="Fetches all transactions associated with an account.",
    response_description="A list of transactions.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def transactions(
    acct: models.Account = Depends(dep.get_account),
    beanfile: models.BeancountFile = Depends(dep.get_beanfile),
    filter=Depends(dep.get_filter),
    search=Depends(dep.get_search_directives),
    priority=Depends(dep.get_mutate_priority),
) -> List[models.Transaction]:
    txns = beanfile.entries.by_account(acct.name).by_type(models.Transaction)
    if priority == dep.MutatePriority.filter:
        return search(filter(txns.__root__))
    else:
        return filter(search(txns.__root__))
