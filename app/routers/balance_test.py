from functools import lru_cache
from ..dependencies import BeanFile, get_beanfile
from ..main import app
from fastapi.testclient import TestClient


@lru_cache
def override():
    return BeanFile("testing/static.beancount")


def test_balance():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    expected_gld = {
        "positions": [
            {
                "units": {"number": 4, "currency": "GLD"},
                "cost": {
                    "number": 105.01,
                    "currency": "USD",
                    "date": "2021-07-08",
                    "label": None,
                },
            },
            {
                "units": {"number": 7, "currency": "GLD"},
                "cost": {
                    "number": 112.74,
                    "currency": "USD",
                    "date": "2021-09-08",
                    "label": None,
                },
            },
            {
                "units": {"number": 7, "currency": "GLD"},
                "cost": {
                    "number": 116.48,
                    "currency": "USD",
                    "date": "2021-10-13",
                    "label": None,
                },
            },
            {
                "units": {"number": 17, "currency": "GLD"},
                "cost": {
                    "number": 119.38,
                    "currency": "USD",
                    "date": "2021-11-22",
                    "label": None,
                },
            },
            {
                "units": {"number": 24, "currency": "GLD"},
                "cost": {
                    "number": 120.26,
                    "currency": "USD",
                    "date": "2022-01-02",
                    "label": None,
                },
            },
        ]
    }
    expected_opening = {
        "positions": [
            {
                "units": {"number": -2845.77, "currency": "USD"},
                "cost": None,
            }
        ]
    }
    expected_pretax = {
        "positions": [
            {
                "units": {"number": -55500, "currency": "IRAUSD"},
                "cost": None,
            }
        ]
    }
    expected_slate = {
        "positions": [
            {
                "units": {"number": -2444.36, "currency": "USD"},
                "cost": None,
            }
        ]
    }

    response = client.get("/balance")
    assert response.status_code == 200
    assert response.json()["Assets:US:ETrade:GLD"] == expected_gld
    assert response.json()["Equity:Opening-Balances"] == expected_opening
    assert response.json()["Income:US:Federal:PreTax401k"] == expected_pretax
    assert response.json()["Liabilities:US:Chase:Slate"] == expected_slate


def test_account():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    expected = {
        "positions": [
            {"units": {"number": -2, "currency": "VACHR"}, "cost": None}
        ]
    }
    response = client.get("/balance/Assets:US:Babble:Vacation")
    assert response.status_code == 200
    assert response.json() == expected

    response = client.get("/balance/Assets:US:Babble:Vacations")
    assert response.status_code == 404
