import jmespath  # type: ignore
import json
import os
import re

from app.dependencies import get_beanfile, _load
from app.internal.beancount import BeancountFile
from app.main import app
from functools import lru_cache


def fetch_account(account: str) -> str:
    with open("testing/realize.json", "r") as f:
        js = json.load(f)
        filter = "children." + ".children.".join(account.split(":"))
        return jmespath.search(filter, js)


def load_static_json() -> str:
    with open("testing/static.json", "r") as f:
        j = f.read()

    path = os.path.join(os.getcwd(), "testing/static.beancount")
    return json.loads(
        re.sub(r"^\/[a-zA-z\/]+\/testing\/static.beancount", path, j)
    )


def load_realize_json() -> str:
    with open("testing/realize.json", "r") as f:
        j = f.read()

    path = os.path.join(os.getcwd(), "testing/static.beancount")
    return json.loads(
        re.sub(r"^\/[a-zA-z\/]+\/testing\/static.beancount", path, j)
    )


@lru_cache
def override():
    return BeancountFile(*_load("testing/static.beancount"))


def setup():
    app.dependency_overrides[get_beanfile] = override
