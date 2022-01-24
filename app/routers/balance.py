from fastapi import APIRouter, Depends, HTTPException, Path
from ..dependencies import get_beanfile
from ..models.data import Inventory
from typing import Dict

router = APIRouter(prefix="/balance", tags=["balances"])


@router.get(
    "/",
    response_model=Dict[str, Inventory],
    summary="Fetch all balances from all accounts",
    response_description="A dictionary of account names and their balances",
)
def balance(
    beanfile=Depends(get_beanfile),
):
    """
    Fetch the balances of all applicable accounts.

    Balances are represented as an Inventory object which contains one or more
    Positions. Refer to the Beancount documentation for more information about
    how inventories work.
    """
    response = {}
    for name, account in beanfile.accounts.items():
        response[name] = account.balance

    return response


@router.get(
    "/{account_name}",
    response_model=Inventory,
    summary="Fetch the balances of an account",
    response_description="A Inventory object representing the account balance",
)
def account(
    account_name: str = Path(
        "", description="The account name to get the balance of"
    ),
    beanfile=Depends(get_beanfile),
):
    """
    Fetch the balance of an account.

    Balances are represented as an Inventory object which contains one or more
    Positions. Refer to the Beancount documentation for more information about
    how inventories work.
    """
    if account_name not in beanfile.accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    return beanfile.accounts[account_name].balance
