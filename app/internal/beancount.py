from beancount import loader
from beancount.core import data, realization
from beancount.query import query
from beancount.query.query_compile import CompilationError
from beancount.query.query_parser import ParseError  # type: ignore
from dataclasses import dataclass
from fastapi.responses import JSONResponse
from jmespath.exceptions import LexerError  # type: ignore
from ..main import app
from typing import Any, Dict, List, Type


@dataclass
class BeancountFile:
    """Provides a representation of a parsed beancount file.

    Attributes:
        entries: The parsed entries.
        errors: Any errors generated during parsing.
        options: The parsed options.
        root: The result of realizing the parsed entries.
    """

    entries: List[data.Directive]
    errors: List[Any]
    options: Dict[str, Any]
    root: realization.RealAccount

    def __init__(
        self,
        entries: List[data.Directive],
        errors: List[Any],
        options: Dict[str, Any],
    ):
        self.entries = entries
        self.errors = errors
        self.options = options
        self.root = realization.realize(entries)

    def account(self, name: str) -> realization.RealAccount:
        """Fetch the given account from the realization.

        Args:
            name: The account name to fetch.

        Returns:
            A `RealAccount` instance of the account or None if not found.
        """
        return realization.get(self.root, name)

    def accounts(self) -> List[str]:
        """Fetches all account names found in the ledger.

        This method works by filtering all held directives to find the Open
        directives and then extracts the account name from each one. Any
        account which exists outside of an Open directive will not be returned.

        Returns:
            A list of account names.
        """
        return [d.account for d in self.filter(data.Open)]

    def filter(self, typ: Type[data.Directive]):
        """Extracts all directives of the given type.

        Args:
            typ: The type of directive to extract from the directives.

        Returns:
            A list of all of the requested directive type.
        """
        return [d for d in self.entries if isinstance(d, typ)]

    def query(self, query_str: str):
        """Queries the ledger with the given query string.

        Args:
            query_str: The BQL query string to use.

        Raises:
            QueryError: If the query fails to compile.

        Returns:
            The result as a tuple of columns and rows.
        """
        try:
            return query.run_query(self.entries, self.options, query_str)
        except (CompilationError, ParseError) as e:
            raise QueryError(str(e))


class QueryError(Exception):
    """Raised when a BQL query fails to compile."""

    pass


def from_file(path: str) -> BeancountFile:
    """Creates a new `BeancountFile` instance using the file at the given path.

    Args:
        path: The full path to the beancount ledger file.

    Returns:
        A new instance of `BeancountFile` with the loaded ledger contents.
    """
    return BeancountFile(*loader.load_file(path))


@app.exception_handler(LexerError)
def jmespath_exception_handler(_, exc: LexerError):
    """Provides an exception handler for catching JMESPath exceptions."""
    return JSONResponse(
        status_code=422,
        content={
            "message": f"Error in JMESPath filter expression: {exc.message}",
            "expression": exc.expression,
            "column": exc.lex_position,
            "token": exc.token_value,
        },
    )
