from __future__ import annotations

from bdantic import models
from fastapi import Request
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .settings import Settings


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

    @staticmethod
    def validate(settings: Settings) -> None:
        """Validates that the provided settings are complete.

        Args:
            settings: The settings to validate.

        Raises:
            ValidationError: If the given settings fail to validate.
        """
        pass


class ValidationError(Exception):
    """Raised when configured settings fail to validate."""

    pass
