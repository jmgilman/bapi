from fastapi import APIRouter, Depends, HTTPException, Path
from ..dependencies import get_beanfile
from ..models.data import Amount
from typing import Dict

router = APIRouter(prefix="/balance", tags=["balances"])


@router.get(
    "/",
    response_model=Dict[str, Dict[str, Amount]],
    summary="Fetch all balances from all accounts",
    response_description="A dictionary of account names and their balances, grouped by currencies",
)
def accounts_balance(
    beanfile=Depends(get_beanfile),
):
    """
    Fetch the balances of all applicable accounts.

    Accounts may have positions in multiple currencies and it is therefore not
    possible to represent a balance with a single result. As such, results from
    this API call contain a dictionary which has the currency of the balance as
    the key and the associated `Amount` as its value.

    Accounts which have a zero balance in a given currency will be excluded from
    the dictionary. If an account has a zero balance across all currencies then
    an empty dictionary is returned.
    """
    response = {}
    for name, account in beanfile.accounts.items():
        response[name] = account.balances

    return response


@router.get(
    "/{account_name}",
    response_model=Dict[str, Dict[str, Amount]],
    summary="Fetch the balances of an account",
    response_description="A dictionary of currency balances and their respective `Amount`'s",
)
def accounts_balance(
    account_name: str = Path("", description="The account name to get the balance of"),
    beanfile=Depends(get_beanfile),
):
    """
    Fetch the balance of an account.

    Accounts may have positions in multiple currencies and it is therefore not
    possible to represent a balance with a single result. As such, results from
    this API call contain a dictionary which has the currency of the balance as
    the key and the associated `Amount` as its value.

    Accounts which have a zero balance in a given currency will be excluded from
    the dictionary. If an account has a zero balance across all currencies then
    an empty dictionary is returned.
    """
    if account_name not in beanfile.accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    return beanfile.accounts[account_name].balances
