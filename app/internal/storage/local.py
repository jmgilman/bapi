from .. import beancount
from ..base import BaseStorage
from bdantic import models

_hash = ""


class LocalStorage(BaseStorage):
    """Provides an interface for loading locally stored beancount ledgers."""

    _hash = ""

    def load(self) -> models.BeancountFile:
        bf = beancount.from_file(self.settings.entry_path())

        LocalStorage._hash = beancount.hash(bf)
        return bf

    @classmethod
    def changed(cls, bf: models.BeancountFile) -> bool:
        return beancount.hash(bf) != cls._hash

    @staticmethod
    def validate(_) -> None:
        pass
