import enum

from app.core import mutate
from bdantic import models
from bdantic.types import ModelDirective
from fastapi import Depends, HTTPException, Path, Query, Request


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


# Map DirectveType to it's actual model type
_TYPE_MAP: dict[DirectiveType, type[ModelDirective]] = {
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


async def authenticated(request: Request) -> None:
    """Validates requests that require authentication.

    Raises:
        HTTPException: If the configured authentication handler fails.
    """
    auth = request.app.state.settings.get_auth()
    assert auth is not None

    if not auth.authenticate(request):
        raise HTTPException(status_code=403)


async def get_beanfile(request: Request) -> models.BeancountFile:
    """Returns the loaded `BeancountFile` instance.

    Returns:
        The loaded `BeancountFile` instance.
    """
    return await request.app.state.cache.beanfile()


def get_directive_type(t: DirectiveType) -> type[ModelDirective]:
    """Converts a `DirectiveType` to it's actual type.

    Args:
        t: The `DirectiveType` to convert.

    Returns:
        The actual directive type.
    """
    return _TYPE_MAP[t]


async def get_account(
    account_name: str = Path("", description="The account name"),
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


def get_directives_mutator(
    filter: str
    | None = Query(
        None,
        description="JMESPath filter to filter with",
        example="[?date > `2022-01-01`]",
    ),
    search: str
    | None = Query(
        None,
        description="Text to perform a full text search with",
        example="Home Depot",
    ),
    priority: mutate.MutatePriority = Query(
        mutate.MutatePriority.filter,
        description="Which operation should happen first: filter or search",
    ),
) -> mutate.DirectivesMutator:
    return mutate.DirectivesMutator(filter, search, priority)
