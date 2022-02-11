import jmespath  # type: ignore
import json

from app.dependencies import get_beanfile
from app.routers import account, directive, file, query, realize

from beancount import loader
from bdantic import models
from fastapi import FastAPI
from fastapi.testclient import TestClient
from functools import lru_cache
from typing import Dict


def client() -> TestClient:
    """Returns a new test client for the app.

    Returns:
        A new `TestClient` instance.
    """
    app = FastAPI()
    app.include_router(account.router)
    app.include_router(directive.router)
    app.include_router(file.router)
    app.include_router(query.router)
    app.include_router(realize.router)
    app.dependency_overrides[get_beanfile] = override

    return TestClient(app)


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


@lru_cache
def load_file_json() -> Dict:
    """Loads the static.beancount full JSON dump.

    Returns:
        The JSON dump.
    """
    return json.loads(override().json(by_alias=True, exclude_none=True))


@lru_cache
def load_realize_json() -> Dict:
    """Loads the static.beancount realization JSON dump.

    Returns:
        The JSON dump.
    """
    return json.loads(override().realize().json())


@lru_cache
def load_static_json() -> Dict:
    """Loads the static.beancount directive JSON dump.

    Returns:
        The JSON dump.
    """
    return json.loads(override().entries.json())


@lru_cache
def override():
    """Provides an override for forcing the API to load the test file."""
    return models.BeancountFile.parse(
        loader.load_file("testing/static.beancount")
    )
