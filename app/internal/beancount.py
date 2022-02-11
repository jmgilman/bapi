import os

from beancount import loader
from bdantic import models


def from_file(path: str) -> models.BeancountFile:
    """Creates a new `BeancountFile` instance using the file at the given path.

    Args:
        path: The full path to the beancount ledger file.

    Returns:
        A new instance of `BeancountFile` with the loaded ledger contents.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No ledger file located at {path}")
    return models.BeancountFile.parse(loader.load_file(path))
