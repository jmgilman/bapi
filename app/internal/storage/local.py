from .. import beancount
from ..base import BaseStorage
from bdantic import models
from loguru import logger


class LocalStorage(BaseStorage):
    """Provides an interface for loading locally stored beancount ledgers."""

    def load(self) -> models.BeancountFile:
        logger.info(f"Loading data from {self.settings.entry_path()}")
        bf = beancount.from_file(self.settings.entry_path())
        self._hash = bf.hash()
        return bf

    def changed(self, bf: models.BeancountFile) -> bool:
        return bf.hash() != self._hash
