from __future__ import annotations

from dataclasses import dataclass
import re
import string

from bdantic import models
from bdantic.types import ModelDirective
from typing import Any, Dict, Generic, List, Set, Tuple, TypeVar

T = TypeVar("T")


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


@dataclass
class Searcher(Generic[T]):
    """A class which can perform a full text search across data

    Attributes:
        data: The data to search
    """

    data: T

    def index(self) -> List[Tuple[str, T]]:
        """Creates a searchable index from the configured data.

        Returns:
            A searchable index.
        """
        pass

    def search(self, query: str) -> T:
        """Searches across the configured data and returns the result.

        Args:
            query: The query string to use for searching

        Returns:
            The search result.
        """
        pass


@dataclass
class DirectiveSearcher(Searcher):
    """A class which can create a searchable index from a list of directives.

    Attributes:
        data: The list of directives to index.
    """

    data: models.Directives

    def __init__(self, data: models.Directives):
        self.data = data

    def search(self, query: str) -> models.Directives:
        return models.Directives(
            __root__=FullTextSearch(self.index()).search(query)
        )

    def index(self):
        index: List[Tuple[str, ModelDirective]] = []

        for d in self.data:
            if isinstance(d, models.Balance):
                index.append((d.account, d))
            elif isinstance(d, models.Close):
                index.append((d.account, d))
            elif isinstance(d, models.Commodity):
                index.append((d.currency, d))
            elif isinstance(d, models.Custom):
                continue
            elif isinstance(d, models.Document):
                s = d.account + " " + d.filename.replace("/", " ")
                if d.links:
                    s += " " + " ".join(d.links)
                if d.tags:
                    s += " " + " ".join(d.tags)
                index.append((s, d))
            elif isinstance(d, models.Event):
                index.append((d.type + " " + d.description, d))
            elif isinstance(d, models.Note):
                index.append((d.account + " " + d.comment, d))
            elif isinstance(d, models.Open):
                s = d.account
                if d.currencies:
                    s += " " + " ".join(d.currencies)
                index.append((s, d))
            elif isinstance(d, models.Pad):
                index.append(
                    (
                        d.account + " " + d.source_account,
                        d,
                    )
                )
            elif isinstance(d, models.Price):
                index.append((d.currency, d))
            elif isinstance(d, models.Query):
                index.append((d.name + " " + d.query_string, d))
            elif isinstance(d, models.Transaction):
                s = d.narration
                if d.payee:
                    s += " " + d.payee
                if d.links:
                    s += " " + " ".join(d.links)
                if d.tags:
                    s += " " + " ".join(d.tags)
                index.append((s, d))

        return index
