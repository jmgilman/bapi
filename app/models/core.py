from __future__ import annotations
import datetime

from .data import Inventory
from .directives import Transaction
from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class BeanFileError(BaseModel):
    """Represents an error thrown when parsing a beancount ledger file.

    Attributes:
        filename: The name of the file the error occurred in.
        lineno: The line number the error occurred on.
        message: The error message.
    """

    filename: str
    lineno: int
    message: str

    def __repr__(self):
        return f"{self.filename} ({self.lineno}): {self.message}"

    @staticmethod
    def from_errors(errors: List[Any]) -> Dict[str, List[BeanFileError]]:
        """Converts a list of loader errors to BeanFileError's.

        Errors are grouped together by type with each entry in the dictionary
        containing a list of all occurrences of that error type.

        Args:
            errors: A list of errors returned from the beancount loader.

        Returns:
            A dictionary keyed by error type and containing a list of
            occurrences of that error type. For example:

            {
                'ParserSyntaxError':
                [
                    file.beancount (102: syntax error, unexpected INDENT
                ]
            }
        """
        bean_errors = {}
        for error in errors:
            name = type(error).__name__

            if name not in bean_errors:
                bean_errors[name] = []
            bean_errors[name].append(
                BeanFileError(
                    filename=error.source["filename"],
                    lineno=error.source["lineno"],
                    message=error.message,
                )
            )

        return bean_errors


class Account(BaseModel):
    name: str
    open: datetime.date
    close: Optional[datetime.date]
    balance: Optional[Inventory]
    transactions: List[Transaction] = []
