from fastapi.testclient import TestClient


def test_accounts(client: TestClient, raw_accounts):
    response = client.get("/account")
    assert response.status_code == 200
    assert response.json() == raw_accounts


def test_account(client: TestClient, raw_accounts):
    expected = list(raw_accounts.values())[0]
    name = expected["name"]

    response = client.get(f"/account/{name}")
    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["open"] == expected["open"]
    assert response.json()["balance"] == expected["balance"]

    response = client.get(f"/account/{name}123")
    assert response.status_code == 404


def test_balance(client: TestClient, raw_accounts):
    expected = list(raw_accounts.values())[0]
    name = expected["name"]

    response = client.get(f"/account/{name}/balance")
    assert response.status_code == 200
    assert response.json() == expected["balance"]

    response = client.get(f"/account/{name}123/balance")
    assert response.status_code == 404


def test_transactions(client: TestClient, raw_accounts, raw_entries):
    account = list(raw_accounts.values())[0]
    name = account["name"]

    txns = [e for e in raw_entries if e["ty"] == "Transaction"]
    expected = list(
        filter(
            lambda t: any(p["account"] == name for p in t["postings"]), txns
        )
    )

    response = client.get(f"/account/{name}/transactions")
    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(f"/account/{name}123/transactions")
    assert response.status_code == 404
