import jwt

from beancount import loader
from beancount.core import data, realization
from beancount.query import query
from beancount.query.query_compile import CompilationError
from beancount.query.query_parser import ParseError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from functools import lru_cache
from .models.core import (
    Account,
    BeanFileError,
    QueryColumn,
    QueryError,
    QueryResult,
)
from .models.directives import Directives
from .models.data import Supported as SupportedData
from .models.data import to_model as to_data_model
from .models.directives import to_model as to_directive_model
from .settings import bean_file, settings
from typing import Any, Dict, List


class BeanFile:
    """Represents the loaded contents of a beancount ledger file.

    This class acts as a helper class which processes results from loading a
    ledger file into a dependency that can be used across API requests. The
    contents of the ledger file are automatically converted to their equivalent
    pydantic models to be returned by the API. Additionally, some processing is
    done in breaking up directives and accounts in order to make accessing some
    data easier.

    Attributes:
        errors: Errors returned by the beancount loader. See BeanFileError.
        options: All options contained within the beancount ledger file.
        directives: All directive entries in the beancount ledger file.
        raw_directives: All directive in their original beancount types.
        accounts: All accounts contained within the beancount ledger file.
    """

    errors: Dict[str, BeanFileError]
    options: Dict[str, Any] = []
    directives: Directives = None
    raw_directives: List[data.Directive] = []
    accounts: Dict[str, Account] = {}

    def __init__(self, filepath: str):
        entries, errors, options = _load(filepath)

        self.directives = Directives(
            to_directive_model(directive) for directive in entries
        )
        self.raw_directives = entries
        self.errors = BeanFileError.from_errors(errors)
        self.options = options

        realized = realization.realize(self.raw_directives)
        for real_account in realization.iter_children(realized, True):
            txns = []
            open = None
            close = None
            for t in real_account.txn_postings:
                if isinstance(t, data.TxnPosting):
                    txns.append(to_directive_model(t.txn))
                elif isinstance(t, data.Open):
                    open = t.date
                elif isinstance(t, data.Close):
                    close = t.date

            self.accounts[real_account.account] = Account(
                name=real_account.account,
                open=open,
                close=close,
                balance=[
                    to_data_model(position)
                    for position in real_account.balance
                ],
                transactions=txns,
            )

    def query(self, query_str: str):
        """Queries the beancount data using the given BQL query string.

        Args:
            query_str: The BQL query string to use

        Returns:
            A QueryResult containing the results of the query

        Raises:
            QueryError: Raised when a query fails to compile or execute
        """
        try:
            result = query.run_query(
                self.raw_directives, self.options, query_str
            )
        except (CompilationError, ParseError) as e:
            raise QueryError(str(e))

        columns = []
        for column in result[0]:
            columns.append(
                QueryColumn(name=column[0], type=column[1].__name__)
            )

        rows = []
        for row in result[1]:
            new_row = {}
            for field in row._fields:
                value = getattr(row, field)
                if type(value) in SupportedData:
                    value = to_data_model(value)
                new_row[field] = value
            rows.append(new_row)

        return QueryResult(header=columns, rows=rows)


def _load(filepath: str):
    return loader.load_file(filepath)


@lru_cache()
def get_beanfile() -> BeanFile:
    """A cached dependency to ensure a Beanfile is only parsed once."""
    return BeanFile(bean_file)


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
