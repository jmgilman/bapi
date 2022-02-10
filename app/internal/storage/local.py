from .. import beancount
from ..base import BaseStorage
from bdantic import models

_hash = ""


class LocalStorage(BaseStorage):
    """Provides an interface for loading locally stored beancount ledgers."""

    def load(self) -> models.BeancountFile:
        bf = beancount.from_file(self.settings.entry_path())
        self._hash = beancount.hash(bf)
        return bf

    def changed(self, bf: models.BeancountFile) -> bool:
        return beancount.hash(bf) != self._hash
