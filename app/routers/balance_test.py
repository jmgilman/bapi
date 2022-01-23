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

    expected = {
        "Assets:US:Babble:Vacation": {
            "VACHR": {"number": -2, "currency": "VACHR"}
        },
        "Assets:US:BofA:Checking": {
            "USD": {"number": 2035.9, "currency": "USD"}
        },
        "Assets:US:ETrade:Cash": {
            "USD": {"number": 444.51, "currency": "USD"}
        },
        "Assets:US:ETrade:GLD": {"GLD": {"number": 59, "currency": "GLD"}},
        "Assets:US:ETrade:ITOT": {"ITOT": {"number": 80, "currency": "ITOT"}},
        "Assets:US:ETrade:VEA": {"VEA": {"number": 111, "currency": "VEA"}},
        "Assets:US:ETrade:VHT": {"VHT": {"number": 26, "currency": "VHT"}},
        "Assets:US:Federal:PreTax401k": {
            "IRAUSD": {"number": 17300.0, "currency": "IRAUSD"}
        },
        "Assets:US:Vanguard:Cash": {
            "USD": {"number": -0.01, "currency": "USD"}
        },
        "Assets:US:Vanguard:RGAGX": {
            "RGAGX": {"number": 225.174, "currency": "RGAGX"}
        },
        "Assets:US:Vanguard:VBMPX": {
            "VBMPX": {"number": 121.559, "currency": "VBMPX"}
        },
        "Equity:Opening-Balances": {
            "USD": {"number": -2845.77, "currency": "USD"}
        },
        "Expenses:Financial:Commissions": {
            "USD": {"number": 232.7, "currency": "USD"}
        },
        "Expenses:Financial:Fees": {
            "USD": {"number": 100.0, "currency": "USD"}
        },
        "Expenses:Food:Alcohol": {"USD": {"number": 79.42, "currency": "USD"}},
        "Expenses:Food:Coffee": {"USD": {"number": 116.17, "currency": "USD"}},
        "Expenses:Food:Groceries": {
            "USD": {"number": 4730.77, "currency": "USD"}
        },
        "Expenses:Food:Restaurant": {
            "USD": {"number": 8822.2, "currency": "USD"}
        },
        "Expenses:Health:Dental:Insurance": {
            "USD": {"number": 156.6, "currency": "USD"}
        },
        "Expenses:Health:Life:GroupTermLife": {
            "USD": {"number": 1313.28, "currency": "USD"}
        },
        "Expenses:Health:Medical:Insurance": {
            "USD": {"number": 1478.52, "currency": "USD"}
        },
        "Expenses:Health:Vision:Insurance": {
            "USD": {"number": 2284.2, "currency": "USD"}
        },
        "Expenses:Home:Electricity": {
            "USD": {"number": 1560.0, "currency": "USD"}
        },
        "Expenses:Home:Internet": {
            "USD": {"number": 1920.07, "currency": "USD"}
        },
        "Expenses:Home:Phone": {"USD": {"number": 1446.3, "currency": "USD"}},
        "Expenses:Home:Rent": {"USD": {"number": 57600.0, "currency": "USD"}},
        "Expenses:Taxes:Y2020:US:CityNYC": {
            "USD": {"number": 4722.84, "currency": "USD"}
        },
        "Expenses:Taxes:Y2020:US:Federal:PreTax401k": {
            "IRAUSD": {"number": 18500.0, "currency": "IRAUSD"}
        },
        "Expenses:Taxes:Y2020:US:Medicare": {
            "USD": {"number": 2878.74, "currency": "USD"}
        },
        "Expenses:Taxes:Y2020:US:SDI": {
            "USD": {"number": 30.24, "currency": "USD"}
        },
        "Expenses:Taxes:Y2020:US:SocSec": {
            "USD": {"number": 7000.04, "currency": "USD"}
        },
        "Expenses:Taxes:Y2020:US:State": {
            "USD": {"number": 10314.57, "currency": "USD"}
        },
        "Expenses:Taxes:Y2021:US:CityNYC": {
            "USD": {"number": 4547.92, "currency": "USD"}
        },
        "Expenses:Taxes:Y2021:US:Federal:PreTax401k": {
            "IRAUSD": {"number": 18500.0, "currency": "IRAUSD"}
        },
        "Expenses:Taxes:Y2021:US:Medicare": {
            "USD": {"number": 2772.12, "currency": "USD"}
        },
        "Expenses:Taxes:Y2021:US:SDI": {
            "USD": {"number": 29.12, "currency": "USD"}
        },
        "Expenses:Taxes:Y2021:US:SocSec": {
            "USD": {"number": 7000.04, "currency": "USD"}
        },
        "Expenses:Taxes:Y2021:US:State": {
            "USD": {"number": 9492.08, "currency": "USD"}
        },
        "Expenses:Taxes:Y2022:US:CityNYC": {
            "USD": {"number": 174.92, "currency": "USD"}
        },
        "Expenses:Taxes:Y2022:US:Federal:PreTax401k": {
            "IRAUSD": {"number": 1200.0, "currency": "IRAUSD"}
        },
        "Expenses:Taxes:Y2022:US:Medicare": {
            "USD": {"number": 106.62, "currency": "USD"}
        },
        "Expenses:Taxes:Y2022:US:SDI": {
            "USD": {"number": 1.12, "currency": "USD"}
        },
        "Expenses:Taxes:Y2022:US:SocSec": {
            "USD": {"number": 281.54, "currency": "USD"}
        },
        "Expenses:Taxes:Y2022:US:State": {
            "USD": {"number": 365.08, "currency": "USD"}
        },
        "Expenses:Transport:Tram": {
            "USD": {"number": 2760.0, "currency": "USD"}
        },
        "Expenses:Vacation": {"VACHR": {"number": 272, "currency": "VACHR"}},
        "Income:US:Babble:GroupTermLife": {
            "USD": {"number": -1313.28, "currency": "USD"}
        },
        "Income:US:Babble:Match401k": {
            "USD": {"number": -19100.0, "currency": "USD"}
        },
        "Income:US:Babble:Salary": {
            "USD": {"number": -249230.52, "currency": "USD"}
        },
        "Income:US:Babble:Vacation": {
            "VACHR": {"number": -270, "currency": "VACHR"}
        },
        "Income:US:ETrade:GLD:Dividend": {},
        "Income:US:ETrade:ITOT:Dividend": {},
        "Income:US:ETrade:PnL": {
            "USD": {"number": -295.85, "currency": "USD"}
        },
        "Income:US:ETrade:VEA:Dividend": {
            "USD": {"number": -128.57, "currency": "USD"}
        },
        "Income:US:ETrade:VHT:Dividend": {
            "USD": {"number": -138.19, "currency": "USD"}
        },
        "Income:US:Federal:PreTax401k": {
            "IRAUSD": {"number": -55500, "currency": "IRAUSD"}
        },
        "Liabilities:AccountsPayable": {},
        "Liabilities:US:Chase:Slate": {
            "USD": {"number": -2444.36, "currency": "USD"}
        },
    }

    response = client.get("/balance")
    assert response.status_code == 200
    assert response.json() == expected


def test_account():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    expected = {"VACHR": {"number": -2, "currency": "VACHR"}}
    response = client.get("/balance/Assets:US:Babble:Vacation")
    assert response.status_code == 200
    assert response.json() == expected

    response = client.get("/balance/Assets:US:Babble:Vacations")
    assert response.status_code == 404
