from ...beancount import BeancountFile, from_file
from ...storage import BaseStorage


class LocalStorage(BaseStorage):
    """Provides an interface for loading locally stored beancount ledgers."""

    def load(self) -> BeancountFile:
        return from_file(self.settings.entry_path())
