from .. import beancount
from ..base import BaseStorage
from bdantic import models


class LocalStorage(BaseStorage):
    """Provides an interface for loading locally stored beancount ledgers."""

    def load(self) -> models.BeancountFile:
        bf = beancount.from_file(self.settings.entry_path())
        self._hash = bf.hash()
        return bf

    def changed(self, bf: models.BeancountFile) -> bool:
        return bf.hash() != self._hash
