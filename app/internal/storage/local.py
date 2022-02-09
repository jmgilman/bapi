from ..beancount import from_file
from ..base import BaseStorage
from bdantic import models


class LocalStorage(BaseStorage):
    """Provides an interface for loading locally stored beancount ledgers."""

    def load(self) -> models.BeancountFile:
        return from_file(self.settings.entry_path())

    @classmethod
    def validate(cls, _):
        pass
