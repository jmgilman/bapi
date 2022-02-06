import enum

from beancount.core import realization
from bdantic import models
from fastapi import Depends, HTTPException, Path, Query, Request
from .internal.beancount import BeancountFile
from .internal.settings import settings
from typing import Callable, Optional, TypeVar

T = TypeVar("T", bound="models.base.BaseList")


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


def authenticated(request: Request) -> None:
    """Validates requests that require authentication.

    Raises:
        HTTPException: If the configured authentication handler fails.
    """
    auth = settings.get_auth()
    assert auth is not None

    if not auth.authenticate(request):
        raise HTTPException(status_code=403)


def get_beanfile() -> BeancountFile:
    """Returns the loaded `BeancountFile` instance.

    Returns:
        The loaded `BeancountFile` instance.
    """
    return settings.beanfile


def get_directives(
    directive: DirectiveType = Path(
        "", description="The type of directive to fetch"
    ),
    beanfile: BeancountFile = Depends(get_beanfile),
) -> Optional[models.Directives]:
    """Filters out all directives not matching the requested type.

    Args:
        directive: The directive type to filter against.

    Returns:
        A list of filtered directives.
    """
    m = models.Directives.parse(beanfile.entries)
    return get_filter(f"[?ty == `{directive.capitalize()}`]")(m)


def get_filter(
    query: Optional[str] = Query(
        None,
        alias="filter",
        description="A JMESPath filter to apply to the results",
        example="[?date > `2022-01-01`]",
    )
) -> Callable[[T], Optional[T]]:
    """Generates a function for filtering a list of models with a query.

    Args:
        query: The JMESPath expression to use for filtering.

    Returns:
        A function that filters a list of models using the given query.
    """

    def apply_filter(m: T):
        if query:
            return m.filter(query)
        else:
            return m

    return apply_filter


def get_real_account(
    account_name: str = Path("", description="The account name to lookup"),
    beanfile=Depends(get_beanfile),
) -> realization.RealAccount:
    """Fetches the given account from a realization.

    Args:
        account_name: The account name to fetch.

    Raises:
        HTTPException: If the account was not found in the realization.

    Returns:
        A `realization.RealAccount` instance."""
    real_acct = beanfile.account(account_name)
    if real_acct is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return real_acct
