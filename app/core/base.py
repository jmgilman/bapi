from __future__ import annotations

from typing import TYPE_CHECKING

from bdantic import models
from fastapi import Request

if TYPE_CHECKING:
    from app.core.settings import Settings


class BaseAuth:
    """Base class for authentication providers.

    Attributes:
        settings: An instance of `Settings` containing the configured settings.
    """

    settings: Settings

    def __init__(self, settings: Settings):
        self.settings = settings

    def authenticate(self, request: Request) -> bool:
        """Authenticates the given request using the configured settings.

        Args:
            request: The HTTP request.

        Returns:
            True if authenticated, false otherwise.
        """
        pass

    @staticmethod
    def validate(settings: Settings) -> None:
        """Validates that the provided settings are complete.

        Args:
            settings: The settings to validate.

        Raises:
            ValidationError: If the given settings fail to validate.
        """
        pass


class BaseStorage:
    """Base class for storage providers.

    Attributes:
        settings: An instance of `Settings` containing the configured settings.
    """

    settings: Settings

    def __init__(self, settings: Settings):
        self.settings = settings

    def load(self) -> models.BeancountFile:
        """Returns a new instance of `BeancountFile` with the loaded ledger.

        Returns:
            A `BeancountFile` instance with the loaded ledger contents.
        """
        pass

    def changed(self, bf: models.BeancountFile) -> bool:
        """Returns if the underlying storage has changed.

        Args:
            bf: The `BeancountFile` instance used to compare for changes.

        Returns:
            True if a change is detected, False otherwise.
        """
        pass


class ValidationError(Exception):
    """Raised when configured settings fail to validate."""

    pass
