from __future__ import annotations

from .beancount import BeancountFile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..settings import Settings


class BaseStorage:
    """Base class for storage providers.

    Attributes:
        settings: An instance of `Settings` containing the configured settings.
    """

    settings: Settings

    def __init__(self, settings: Settings):
        self.settings = settings

    def load(self) -> BeancountFile:
        """Returns a new instance of `BeancountFile` with the loaded ledger.

        Returns:
            A `BeancountFile` instance with the loaded ledger contents.
        """
        pass
