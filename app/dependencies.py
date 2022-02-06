import enum
import jwt

from beancount import loader
from beancount.core import data, realization
from bdantic import models
from fastapi import Depends, HTTPException, Path, Query
from fastapi.security import HTTPBearer
from .internal.beancount import BeancountFile
from functools import lru_cache
from .settings import bean_file, settings
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

T = TypeVar("T", bound="models.base.BaseList")


class DirectiveType(str, enum.Enum):
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


def _load(filepath: str) -> Tuple[List[data.Directive], List, Dict[str, Any]]:
    return loader.load_file(filepath)


@lru_cache()
def get_beanfile() -> BeancountFile:
    """A cached dependency to ensure a BeancountFile is only parsed once."""
    return BeancountFile(*_load(bean_file))


bearer = HTTPBearer()


def authenticated(token=Depends(bearer)):
    """Dependency for validating requests that contain a JWT token."""
    if settings.jwt:
        client = jwt.PyJWKClient(settings.jwt.jwks)
        signing_key = client.get_signing_key_from_jwt(token.credentials).key

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=settings.jwt.algorithms.split(","),
                audience=settings.jwt.audience,
                issuer=settings.jwt.issuer,
            )
        except jwt.exceptions.DecodeError as e:
            raise HTTPException(status_code=403, detail=str(e))

        return payload


def get_directives(
    directive: DirectiveType = Path(
        "", description="The type of directive to fetch"
    ),
    beanfile: BeancountFile = Depends(get_beanfile),
) -> Optional[models.Directives]:
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
    real_acct = beanfile.account(account_name)
    if real_acct is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return real_acct
