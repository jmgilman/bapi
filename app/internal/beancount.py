from beancount import loader
from bdantic.models import BeancountFile


def from_file(path: str) -> BeancountFile:
    """Creates a new `BeancountFile` instance using the file at the given path.

    Args:
        path: The full path to the beancount ledger file.

    Returns:
        A new instance of `BeancountFile` with the loaded ledger contents.
    """
    return BeancountFile.parse(loader.load_file(path))
