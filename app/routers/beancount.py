from beancount.core import data, getters, realization
from ..dependencies import get_entries
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from ..models.beancount import Account, Amount, Transaction
from typing import Dict, List

router = APIRouter()


@router.get(
    "/balances",
    response_model=Dict[str, Dict[str, Amount]],
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
        inventory = {}
        for currency in account.balance.currencies():
            inventory[currency] = Amount.from_bean(
                account.balance.get_currency_units(currency)
            )
        balances[account.account] = inventory

    return balances


@router.get(
    "/balance/{account_name}",
    response_model=Dict[str, Amount],
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

    inventory = {}
    for currency in account.balance.currencies():
        inventory[currency] = Amount.from_bean(
            account.balance.get_currency_units(currency)
        )

    return inventory


@router.get("/accounts", response_model=List[str])
def accounts(entries=Depends(get_entries)):
    return list(getters.get_accounts(entries))


@router.get("/account/{account_name}", response_model=Account)
def account(account_name: str, entries=Depends(get_entries)):
    accounts = realization.realize(entries)
    account = realization.get(accounts, account_name)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    # TODO: Support inventories with multiple positions
    try:
        position = account.balance.get_only_position()
        balance = Amount(
            number=float(position.units.number), currency=position.units.currency
        )
    except AssertionError:
        balance = None

    txns = []
    open = None
    close = None
    for t in account.txn_postings:
        if isinstance(t, data.TxnPosting):
            txns.append(Transaction.from_bean(t.txn))
        elif isinstance(t, data.Open):
            open = t.date
        elif isinstance(t, data.Close):
            close = t.date

    return Account(
        name=account_name, balance=balance, open=open, close=close, transactions=txns
    )


@router.get("/transactions")
def transactions(entries=Depends(get_entries)):
    txns = []
    for txn in data.filter_txns(entries):
        txns.append(Transaction.from_bean(txn))

    return txns
