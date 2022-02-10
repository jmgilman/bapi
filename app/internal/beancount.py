import os

from beancount import loader
from bdantic import models
from typing import cast, List


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


def hash(bf: models.BeancountFile) -> str:
    """Calculates a hash of the underlying beancount ledger files.

    Args:
        bf: The `BeancountFile` to calculate a hash for.

    Returns:
        An MD5 hex digest.
    """
    filenames = cast(List[str], bf.options.__root__.get("include", []))
    return loader.compute_input_hash(filenames)
