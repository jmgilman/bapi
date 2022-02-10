import enum

from .internal.settings import settings
from .internal.search import search_accounts, search_directives, Directives
from bdantic import models
from bdantic.types import ModelDirective
from fastapi import Depends, HTTPException, Path, Query, Request
from typing import Callable, Dict, List, Optional, Type, TypeVar, Union

Filterable = Union[
    models.base.BaseList, List[ModelDirective], List[models.TxnPosting]
]
T = TypeVar("T", bound="Filterable")


class DirectiveType(str, enum.Enum):
    """An enum of valid values when specifying a directive type."""

    balance = "balance"
    close = "close"
    commodity = "commodity"
    custom = "custom"
    document = "document"
    event = "event"
    note = "note"
    open = "open"
    pad = "pad"
    price = "price"
    query = "query"
    transaction = "transaction"


class MutatePriority(str, enum.Enum):
    """An enum controlling the order in which filtering/searching occurs."""

    filter = "filter"
    search = "search"


# Map DirectveType to it's actual model type
_TYPE_MAP: Dict[DirectiveType, Type[ModelDirective]] = {
    DirectiveType.balance: models.Balance,
    DirectiveType.close: models.Close,
    DirectiveType.commodity: models.Commodity,
    DirectiveType.custom: models.Custom,
    DirectiveType.document: models.Document,
    DirectiveType.event: models.Event,
    DirectiveType.note: models.Note,
    DirectiveType.open: models.Open,
    DirectiveType.pad: models.Pad,
    DirectiveType.price: models.Price,
    DirectiveType.query: models.Query,
    DirectiveType.transaction: models.Transaction,
}


def get_beanfile() -> models.BeancountFile:
    """Returns the loaded `BeancountFile` instance.

    Returns:
        The loaded `BeancountFile` instance.
    """
    return settings.beanfile


def authenticated(request: Request) -> None:
    """Validates requests that require authentication.

    Raises:
        HTTPException: If the configured authentication handler fails.
    """
    auth = settings.get_auth()
    assert auth is not None

    if not auth.authenticate(request):
        raise HTTPException(status_code=403)


def get_account(
    account_name: str = Path("", description="The account name to lookup"),
    beanfile: models.BeancountFile = Depends(get_beanfile),
) -> models.Account:
    """Returns an `Account` instance for the given account name.

    Args:
        account_name: The name of the account.

    Raises:
        HTTPException: If the account was not found.

    Returns:
        An `Account` instance of the given account name."""
    if account_name not in beanfile.accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    return beanfile.accounts[account_name]


def get_directives(
    directive: DirectiveType = Path(
        "", description="The type of directive to fetch"
    ),
    beanfile: models.BeancountFile = Depends(get_beanfile),
) -> models.Directives:
    """Filters out all directives not matching the requested type.

    Args:
        directive: The directive type to filter against.

    Returns:
        A filtered `Directives` instance.
    """
    return beanfile.entries.by_type(_TYPE_MAP[directive])  # type: ignore


def get_filter(
    query: Optional[str] = Query(
        None,
        alias="filter",
        description="A JMESPath filter to apply to the results",
        example="[?date > `2022-01-01`]",
    )
) -> Callable[[T], T]:
    """Generates a function for filtering a list of models with a query.

    Args:
        query: The JMESPath expression to use for filtering.

    Returns:
        A function that filters a list of models using the given query.
    """

    def apply_filter(m: T):
        if query:
            if isinstance(m, models.base.BaseList):
                return m.filter(query)
            elif isinstance(m, list) and m:
                if isinstance(m[0], models.TxnPosting):
                    filtered_txns = models.realize.TxnPostings(
                        __root__=m
                    ).filter(query)
                    if filtered_txns:
                        return filtered_txns.__root__
                    else:
                        return []
                else:
                    filtered_dirs = models.Directives(__root__=m).filter(query)
                    if filtered_dirs:
                        return filtered_dirs.__root__
                    else:
                        return []
        else:
            return m

    return apply_filter


def get_mutate_priority(
    priority: MutatePriority = Query(
        MutatePriority.filter,
        description="Which operation should happen first: filter or search",
    )
) -> MutatePriority:
    """Returns the desired priority for searching and filtering.

    Args:
        priority: The `MutatePriority` to use.

    Returns:
        The provided `MutatePriority`.
    """
    return priority


def get_real_account(
    account_name: str = Path("", description="The account name to lookup"),
    beanfile: models.BeancountFile = Depends(get_beanfile),
) -> models.RealAccount:
    """Fetches the given account from a realization.

    Args:
        account_name: The account name to fetch.

    Raises:
        HTTPException: If the account was not found in the realization.

    Returns:
        A `RealAccount` instance."""
    account = beanfile.realize().get(account_name)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account


def get_search_accounts(
    search: Optional[str] = Query(
        None,
        description="A string to search across results with",
        example="Assets",
    )
) -> Callable[[List[str]], Optional[List[str]]]:
    """Generates a function for running a full text search across accounts.

    Args:
        search: A string to search across accounts with.

    Returns:
        A function that searches across accounts.
    """

    def apply_search(accounts: List[str]):
        if search:
            return search_accounts(accounts).search(search)
        else:
            return accounts

    return apply_search


def get_search_directives(
    search: Optional[str] = Query(
        None,
        description="A string to search across results with",
        example="Home Depot",
    )
) -> Callable[[Directives], Optional[Directives]]:
    """Generates a function for running a full text search across directives.

    Args:
        search: A string to search across directives with.

    Returns:
        A function that searches across directives.
    """

    def apply_search(directives: Directives):
        if search:
            return search_directives(directives).search(search)
        else:
            return directives

    return apply_search
