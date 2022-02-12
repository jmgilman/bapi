import enum
from typing import Dict, Type

from bdantic import models
from bdantic.types import ModelDirective


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


def get_directive_type(t: DirectiveType) -> Type[ModelDirective]:
    """Converts a `DirectiveType` to it's actual type.

    Args:
        t: The `DirectiveType` to convert.

    Returns:
        The actual directive type.
    """
    return _TYPE_MAP[t]
