import jmespath  # type: ignore
import json
import os
import re

from app.dependencies import get_beanfile
from app.main import app
from beancount import loader
from bdantic import models
from functools import lru_cache


def fetch_account(account: str) -> str:
    """Fetches the given account from the realization JSON dump.

    Args:
        account: The account name to fetch.

    Returns:
        The fetched account.
    """
    js = load_realize_json()
    filter = "children." + ".children.".join(account.split(":"))
    return jmespath.search(filter, js)


def load_static_json() -> str:
    """Loads the static.beancount JSON dump.

    Returns:
        The JSON dump.
    """
    with open("testing/static.json", "r") as f:
        j = f.read()

    path = os.path.join(os.getcwd(), "testing/static.beancount")
    return json.loads(
        re.sub(r"\/[a-zA-z\/]+\/testing\/static.beancount", path, j)
    )


def load_realize_json() -> str:
    """Loads the static.beancount realization JSON dump.

    Returns:
        The JSON dump.
    """
    with open("testing/realize.json", "r") as f:
        j = f.read()

    path = os.path.join(os.getcwd(), "testing/static.beancount")
    return json.loads(
        re.sub(r"\/[a-zA-z\/]+\/testing\/static.beancount", path, j)
    )


@lru_cache
def override():
    """Provides an override for forcing the API to load the test file."""
    return models.BeancountFile.parse(
        loader.load_file("testing/static.beancount")
    )


def setup():
    """Overrides the get_beanfile dependency to use the test file."""
    app.dependency_overrides[get_beanfile] = override
