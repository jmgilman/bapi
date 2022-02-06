import re
import string

from beancount.core import data
from typing import Dict, List, Set


class FullTextSearch:
    """Indexes transactions and provides full-text search across them.

    The index is initialized using the list of transactions passed to the class
    constructor. A rudimentary full-text search is made available by indexing
    words found across all transaction payee and narration fields. The search
    method can be used for searching the index.
    """

    def __init__(self, txs: List[data.Transaction]):
        """Initializes the internal index with the given list of transactions.

        Args:
            txs: The list of transactions to initialize the index with.
        """
        self._index: Dict[str, Set[int]] = {}
        self._transactions: Dict[int, data.Transaction] = {}
        self._index_transactions(txs)

    def search(self, query: str):
        """Searches the index using the given query string.

        The query string is broken up into tokens (words) and then each token
        is analyzed against the index to find transactions which contain the
        token. For a transaction to be returned it must contain all analyzed
        tokens. For example, the more tokens passed, the more constrained the
        search becomes.

        Args:
            query: The query string to search with.

        Returns:
            A list of transactions which satisfy the given search query.
        """
        tokens = self._tokenize(query)
        indexes = [self._index.get(token, set()) for token in tokens]
        return [self._transactions[id] for id in set.intersection(*indexes)]

    def _index_transactions(self, txs: List[data.Transaction]):
        """Populates the internal index using the given transactions."""
        for tx_id, tx in enumerate(txs):
            full_text = " ".join([(tx.narration or ""), (tx.payee or "")])
            tokens = self._tokenize(full_text)

            if tx_id not in self._transactions:
                self._transactions[tx_id] = tx

            for token in tokens:
                if token not in self._index:
                    self._index[token] = set()
                self._index[token].add(tx_id)

    def _tokenize(self, full_text: str):
        """Breaks up a string into its token components."""
        punc = re.compile("[%s]" % re.escape(string.punctuation))

        tokens = full_text.split()
        tokens = [token.lower() for token in tokens]
        tokens = [punc.sub("", token) for token in tokens]

        return tokens


def txn_has_account(txn: data.Transaction, account: str):
    for posting in txn.postings:
        if posting.account == account:
            return True

    return False
