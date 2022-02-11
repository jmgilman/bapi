from .internal.mutate import DirectivesMutator, MutatePriority
from bdantic import models
from fastapi import Depends, HTTPException, Path, Query, Request
from typing import Optional


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
    filter: Optional[str] = Query(
        None,
        description="JMESPath filter to filter with",
        example="[?date > `2022-01-01`]",
    ),
    search: Optional[str] = Query(
        None,
        description="Text to perform a full text search with",
        example="Home Depot",
    ),
    priority: MutatePriority = Query(
        MutatePriority.filter,
        description="Which operation should happen first: filter or search",
    ),
) -> DirectivesMutator:
    return DirectivesMutator(filter, search, priority)
