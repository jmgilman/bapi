from fastapi import APIRouter, Depends, HTTPException, Path
from ..dependencies import get_beanfile
from ..models.core import Account
from typing import List

router = APIRouter(prefix="/account", tags=["accounts"])


@router.get(
    "/",
    response_model=List[str],
    summary="Fetch a list of all account names",
    response_description="A list of all account names",
)
def accounts(beanfile=Depends(get_beanfile)):
    """Fetches and returns a list of all accounts in the ledger file."""
    return list(beanfile.accounts.keys())


@router.get(
    "/{account_name}",
    response_model=Account,
    summary="Fetch the details of an account.",
    response_description="An `Account` containing the given account details",
)
def account(
    account_name: str = Path("", description="The account name to lookup"),
    beanfile=Depends(get_beanfile),
):
    """Fetches and returns various details about an account in the ledger file."""
    if account_name not in beanfile.accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    return beanfile.accounts[account_name]
