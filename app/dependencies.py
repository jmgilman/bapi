import itertools
import os

from beancount import loader
from beancount.core import data, realization
from functools import lru_cache
from .models.core import Account, BeanFileError
from .models.directives import Directives
from .models.data import to_model as to_data_model
from .models.directives import to_model as to_directive_model
from .settings import bean_file
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
            balances = {}
            for currency in real_account.balance.currencies():
                balances[currency] = to_data_model(
                    real_account.balance.get_currency_units(currency)
                )

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
                balances=balances,
                transactions=txns,
            )


def _load(filepath: str):
    return loader.load_file(filepath)


@lru_cache()
def get_beanfile() -> BeanFile:
    """A cached dependency to ensure a Beanfile is only parsed once."""
    return BeanFile(bean_file)
