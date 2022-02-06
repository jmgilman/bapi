from bdantic.models.data import Inventory
from bdantic.models.directives import Transaction, TxnPosting
from bdantic.models.realize import Account, RealAccount
from beancount.core import realization
from ..dependencies import get_beanfile, get_real_account
from fastapi import APIRouter, Depends
from typing import cast, Dict, List

router = APIRouter(prefix="/account", tags=["accounts"])


@router.get(
    "/",
    response_model=List[str],
    summary="Fetch a list of all account names",
    response_description="A list of all account names.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
def accounts(beanfile=Depends(get_beanfile)) -> List[str]:
    return list(beanfile.accounts())


@router.get(
    "/{account_name}",
    response_model=Account,
    summary="Fetch the details of an account.",
    response_description="An `Account` containing the given account details.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
def account(
    real_acct: realization.RealAccount = Depends(get_real_account),
) -> Account:
    return RealAccount.parse(real_acct).to_account()


@router.get(
    "/{account_name}/balance",
    response_model=Dict[str, Inventory],
    summary="Fetch the balance of an account.",
    response_description="A mapping of currencies to lists of positions.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
def balance(
    real_acct: realization.RealAccount = Depends(get_real_account),
) -> Dict[str, Inventory]:
    return RealAccount.parse(real_acct).to_account().balance


@router.get(
    "/{account_name}/realize",
    response_model=RealAccount,
    summary="Fetch the result of realizing an account.",
    response_description="The raw results from calling realization.realize().",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
def realize(
    real_acct: realization.RealAccount = Depends(get_real_account),
) -> RealAccount:
    return RealAccount.parse(real_acct)


@router.get(
    "/{account_name}/transactions",
    response_model=List[Transaction],
    summary="Fetches all transactions associated with an account.",
    response_description="A list of transactions.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
def transactions(
    real_acct: realization.RealAccount = Depends(get_real_account),
) -> List[Transaction]:
    txn_postings = cast(
        List[TxnPosting],
        RealAccount.parse(real_acct).txn_postings.filter(
            "[?ty == 'TxnPosting']"
        ),
    )
    return [tp.txn for tp in txn_postings]
