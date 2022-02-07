import re
import string

from beancount.core import data
from bdantic import models
from bdantic.types import ModelDirective
from typing import Any, Dict, List, Set, Tuple, Union


class FullTextSearch:
    """Indexes a list of objects and provides full-texth search across them.

    The index is built using the data given during initialization. The expected
    data format is a list of tuples where the first entry is a string and the
    second entry is an object to associate with the string. The index is then
    constructed by tokenizing the string and associating the result with the
    object. The result is a searchable index.
    """

    def __init__(self, index: List[Tuple[str, Any]]):
        """Creates a new searchable index for the given list of objects.

        Args:
            index: A list of tuples where the first entry is a searchable
                string and the second entry is an object to associate with that
                searchable string.
        """
        self._entries: Dict[int, Any] = {}
        self._index: Dict[str, Set[int]] = {}

        for eid, entry in enumerate(index):
            self._index_entry(eid, entry[0], entry[1])

    def search(self, query: str):
        """Searches the index using the given query string.

        The query string is broken up into tokens (words) and then each token
        is analyzed against the index to find entries which contain the token.
        For an entry to be returned it must contain all analyzed tokens. For
        example, the more tokens passed, the more constrained the search
        becomes.

        Args:
            query: The query string to search with.

        Returns:
            A list of entries which satisfy the given search query.
        """
        tokens = self._tokenize(query)
        indexes = [self._index.get(token, set()) for token in tokens]
        return [self._entries[id] for id in set.intersection(*indexes)]

    def _index_entry(self, entry_id: int, text: str, entry: Any):
        """Indexes an entry.

        Args:
            entry_id: The unique entry ID.
            text: The text to index with.
            entry: The entry to index.
        """
        tokens = self._tokenize(text)

        if entry_id not in self._entries:
            self._entries[entry_id] = entry

        for token in tokens:
            if token not in self._index:
                self._index[token] = set()
            self._index[token].add(entry_id)

    def _tokenize(self, full_text: str) -> List[str]:
        """Breaks up a string into its token components.

        Args:
            full_text: The string to tokenize.

        Result:
            A list of string tokens.
        """
        punc = re.compile("[%s]" % re.escape(string.punctuation))

        tokens = full_text.split()
        tokens = [token.lower() for token in tokens]
        tokens = [punc.sub("", token) for token in tokens]

        return tokens


Directive = Union[data.Directive, ModelDirective]
Directives = Union[List[Directive], models.Directives]


def search_accounts(accounts: List[str]) -> FullTextSearch:
    """Returns a FullTextSearch instance for the given list of accounts.

    Args:
        accounts: A list of account names to search across.

    Returns:
        A new FullTextSearch instance configured with the account names.
    """
    return FullTextSearch([(a.replace(":", " "), a) for a in accounts])


def search_directives(directives: Directives) -> FullTextSearch:
    """Returns a FullTextSearch instance for the given list of directives.

    Args:
        directives: A list of directives to search across.

    Returns:
        A new FullTextSearch instance configured with the directives.
    """
    index: List[Tuple[str, Directive]] = []
    for d in directives:
        if isinstance(d, data.Balance) or isinstance(d, models.Balance):
            index.append((d.account, d))
        elif isinstance(d, data.Close) or isinstance(d, models.Close):
            index.append((d.account, d))
        elif isinstance(d, data.Commodity) or isinstance(d, models.Commodity):
            index.append((d.currency, d))
        elif isinstance(d, data.Custom) or isinstance(d, models.Custom):
            continue
        elif isinstance(d, data.Document) or isinstance(d, models.Document):
            s = d.account + " " + d.filename.replace("/", " ")
            if d.links:
                s += " " + " ".join(d.links)
            if d.tags:
                s += " " + " ".join(d.tags)
            index.append((s, d))
        elif isinstance(d, data.Event) or isinstance(d, models.Event):
            index.append((d.type + " " + d.description, d))
        elif isinstance(d, data.Note) or isinstance(d, models.Note):
            index.append((d.account + " " + d.comment, d))
        elif isinstance(d, data.Open) or isinstance(d, models.Open):
            s = d.account
            if d.currencies:
                s += " " + " ".join(d.currencies)
            index.append((s, d))
        elif isinstance(d, data.Pad) or isinstance(d, models.Pad):
            index.append(
                (
                    d.account + " " + d.source_account,
                    d,
                )
            )
        elif isinstance(d, data.Price) or isinstance(d, models.Price):
            index.append((d.currency, d))
        elif isinstance(d, data.Query) or isinstance(d, models.Query):
            index.append((d.name + " " + d.query_string, d))
        elif isinstance(d, data.Transaction) or isinstance(
            d, models.Transaction
        ):
            s = d.narration
            if d.payee:
                s += " " + d.payee
            if d.links:
                s += " " + " ".join(d.links)
            if d.tags:
                s += " " + " ".join(d.tags)
            index.append((s, d))

    return FullTextSearch(index)
