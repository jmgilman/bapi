import datetime

from beancount.core import data
from ..dependencies import get_beanfile
from fastapi import APIRouter, Depends
from ..internal.beancount import FullTextSearch, txn_has_account
from ..models.directives import Transaction
from typing import List, Optional

router = APIRouter()


@router.get(
    "/transactions",
    response_model=List[Transaction],
    summary="Fetch all transactions",
    response_description="A list of (potentially filtered) transactions.",
)
def transactions(
    account: Optional[str] = None,
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
    search: Optional[str] = None,
    beanfile=Depends(get_beanfile),
):
    """Fetches all transactions contained within the beancount ledger.

    Various query parameters are available for filtering the resulting list of
    transactions. The parameters are accumulative and a transaction must fit
    the criteria described by all parameters passed in order for it to be
    returned.

    Note that some transactions may have additional metadata associated with
    them that is impossible to serialize into JSON. In these cases the problem
    fields will be stripped from the metadata and not returned in the response.
    """

    def apply(txn: data.Transaction):
        keep = [True]
        if account:
            keep.append(txn_has_account(txn, account))
        if start:
            keep.append(txn.date >= start)
        if end:
            keep.append(txn.date < end)

        return all(keep)

    filtered = list(filter(apply, beanfile.directives.transaction))
    if search:
        fts = FullTextSearch()
        fts.index(filtered)
        return fts.search(search)
    else:
        return filtered
