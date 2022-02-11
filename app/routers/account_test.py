import jmespath  # type: ignore
import pytest

from testing import common as c


@pytest.fixture
def account():
    return "Assets:US:Babble:Vacation"


@pytest.fixture
def client():
    return c.client()


def test_accounts(client):
    j = c.load_static_json()
    expected = sorted(jmespath.search("[?ty == 'Open'].account", j))

    response = client.get("/account")
    assert response.status_code == 200
    assert sorted(response.json()) == expected


def test_account(account, client):
    expected = c.fetch_account(account)
    expected_date = jmespath.search(
        "txn_postings[?ty == 'Open'].date", expected
    )[0]

    response = client.get(f"/account/{account}")
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

    response = client.get(f"/account/{account}123")
    assert response.status_code == 404


def test_balance(account, client):
    expected = c.fetch_account(account)
    expected_balance = {
        expected["balance"][0]["units"]["currency"]: [
            {
                "ty": expected["balance"][0]["ty"],
                "units": expected["balance"][0]["units"],
            }
        ]
    }

    response = client.get(f"/account/{account}/balance")
    assert response.status_code == 200
    assert response.json() == expected_balance

    response = client.get(f"/account/{account}123/balance")
    assert response.status_code == 404


def test_realize(account, client):
    expected = c.fetch_account(account)

    response = client.get(f"/account/{account}/realize")
    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(f"/account/{account}123/realize")
    assert response.status_code == 404


def test_transactions(account, client):
    expected = c.load_static_json()

    response = client.get(f"/account/{account}/transactions")
    assert response.status_code == 200
    assert response.json() == jmespath.search(
        f"[?postings[?account == '{account}']]", expected
    )

    response = client.get(f"/account/{account}123/transactions")
    assert response.status_code == 404
