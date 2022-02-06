import jmespath  # type: ignore
import pytest

from fastapi.testclient import TestClient
from ..main import app
from testing import common as c  # type: ignore


def setup_module(_):
    c.setup()


@pytest.fixture
def account():
    return "Assets:US:Babble:Vacation"


def test_accounts():
    with TestClient(app) as client:
        j = c.load_static_json()
        expected = sorted(jmespath.search("[?ty == 'Open'].account", j))

        response = client.get("/account")
        assert response.status_code == 200
        assert sorted(response.json()) == expected


def test_account(account):
    with TestClient(app) as client:
        expected = c.fetch_account(account)
        expected_date = jmespath.search(
            "txn_postings[?ty == 'Open'].date", expected
        )[0]

        response = client.get("/account/Assets:US:Babble:Vacation")
        assert response.status_code == 200
        assert response.json()["name"] == account
        assert response.json()["open"] == expected_date
        assert response.json()["balance"] == {
            expected["balance"][0]["units"]["currency"]: [
                {
                    "ty": expected["balance"][0]["ty"],
                    "units": expected["balance"][0]["units"],
                }
            ]
        }

        response = client.get("/account/Assets:US:Babble:Vacations")
        assert response.status_code == 404


def test_balance(account):
    with TestClient(app) as client:
        expected = c.fetch_account(account)
        expected_balance = {
            expected["balance"][0]["units"]["currency"]: [
                {
                    "ty": expected["balance"][0]["ty"],
                    "units": expected["balance"][0]["units"],
                }
            ]
        }

        response = client.get("/account/Assets:US:Babble:Vacation/balance")
        assert response.status_code == 200
        assert response.json() == expected_balance

        response = client.get("/account/Assets:US:Babble:Vacations/balance")
        assert response.status_code == 404


def test_realize(account):
    with TestClient(app) as client:
        expected = c.fetch_account(account)

        response = client.get("/account/Assets:US:Babble:Vacation/realize")
        assert response.status_code == 200
        assert response.json() == expected

        response = client.get("/account/Assets:US:Babble:Vacations/realize")
        assert response.status_code == 404


def test_transactions(account):
    with TestClient(app) as client:
        expected = c.fetch_account(account)

        response = client.get(
            "/account/Assets:US:Babble:Vacation/transactions"
        )
        assert response.status_code == 200
        assert response.json() == jmespath.search(
            "[?ty == 'TxnPosting'].txn", expected["txn_postings"]
        )

        response = client.get(
            "/account/Assets:US:Babble:Vacations/transactions"
        )
        assert response.status_code == 404
