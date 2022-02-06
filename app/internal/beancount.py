from beancount.core import data, realization
from beancount.query import query
from beancount.query.query_compile import CompilationError
from beancount.query.query_parser import ParseError  # type: ignore
from dataclasses import dataclass
from typing import Any, Dict, List, Type


@dataclass
class BeancountFile:
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
        return realization.get(self.root, name)

    def accounts(self) -> List[str]:
        return [d.account for d in self.filter(data.Open)]

    def filter(self, typ: Type[data.Directive]):
        return [d for d in self.entries if isinstance(d, typ)]

    def query(self, query_str: str):
        try:
            return query.run_query(self.entries, self.options, query_str)
        except (CompilationError, ParseError) as e:
            raise QueryError(str(e))


class QueryError(Exception):
    pass
