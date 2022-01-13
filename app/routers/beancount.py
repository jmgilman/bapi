from beancount.core import data, getters, realization
from sqlalchemy.sql.expression import desc
from ..dependencies import get_entries
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()


class Balance(BaseModel):
    number: float
    currency: str


@router.get(
    "/balances",
    response_model=Dict[str, Balance],
    summary="Calculate account balances",
    response_description="A dictionary of account names and their respective `Balance`",
)
def balances(
    default_currency: str = Query(
        "USD", description="The currency to use for accounts with a zero balance"
    ),
    entries=Depends(get_entries),
):
    """
    Calculate the balances of all applicable accounts.

    Note that accounts with multiple positions are *not* supported and will
    be skipped in processing resulting in them missing from the final response.
    Accounts which have a balance of zero will still be recorded but will use
    the `default_currency` specified as the currency unit.
    """
    accounts = realization.realize(entries)
    balances = {}
    for account in realization.iter_children(accounts, True):
        # TODO: Support inventories with multiple positions
        try:
            position = account.balance.get_only_position()
        except AssertionError:
            continue

        if position:
            balances[account.account] = Balance(
                number=float(position.units.number), currency=position.units.currency
            )
        else:
            balances[account.account] = Balance(number=0.00, currency=default_currency)

    return balances


@router.get(
    "/balance/{account_name}",
    response_model=Balance,
    summary="Calculate the balance of an account",
    response_description="A `Balance` with the account balance",
)
def balance(
    account_name: str = Path(
        None, description="The name of the account to calculate a balance for"
    ),
    default_currency: str = Query(
        "USD", description="The currency to use for accounts with a zero balance"
    ),
    entries=Depends(get_entries),
):
    """
    Calculates the balance of the given account.

    Note that accounts with multiple positions are not supported and will result
    in an error being returned. Accounts with a zero balance will use the
    `default_currency` specified as the currency unit.
    """
    accounts = realization.realize(entries)
    account = realization.get(accounts, account_name)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    # TODO: Support inventories with multiple positions
    try:
        position = account.balance.get_only_position()
    except AssertionError:
        raise HTTPException(
            status_code=400,
            detail="Accounts with multiple positions are not currently supported",
        )

    if position:
        return Balance(
            number=position.units.number,
            currency=position.units.currency,
        )
    else:
        return Balance(number=0.00, currency=default_currency)


@router.get("/accounts", response_model=List[str])
def accounts(entries=Depends(get_entries)):
    return list(getters.get_accounts(entries))


@router.get("/transactions")
def transactions(entries=Depends(get_entries)):
    txns = []
    for txn in data.filter_txns(entries):
        postings = []
        for posting in txn.postings:
            postings.append(
                {
                    "account": posting.account,
                    "amount": float(posting.units.number),
                    "currency": posting.units.currency,
                }
            )
        txns.append(
            {
                "date": txn.date,
                "flag": txn.flag,
                "payee": txn.payee,
                "narration": txn.narration,
                "postings": postings,
            }
        )

    return txns
