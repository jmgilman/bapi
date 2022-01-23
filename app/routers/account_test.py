from functools import lru_cache
from ..dependencies import BeanFile, get_beanfile
from ..main import app
from fastapi.testclient import TestClient


@lru_cache
def override():
    return BeanFile("testing/static.beancount")


def test_accounts():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    expected = [
        "Assets:US:Babble:Vacation",
        "Assets:US:BofA:Checking",
        "Assets:US:ETrade:Cash",
        "Assets:US:ETrade:GLD",
        "Assets:US:ETrade:ITOT",
        "Assets:US:ETrade:VEA",
        "Assets:US:ETrade:VHT",
        "Assets:US:Federal:PreTax401k",
        "Assets:US:Vanguard:Cash",
        "Assets:US:Vanguard:RGAGX",
        "Assets:US:Vanguard:VBMPX",
        "Equity:Opening-Balances",
        "Expenses:Financial:Commissions",
        "Expenses:Financial:Fees",
        "Expenses:Food:Alcohol",
        "Expenses:Food:Coffee",
        "Expenses:Food:Groceries",
        "Expenses:Food:Restaurant",
        "Expenses:Health:Dental:Insurance",
        "Expenses:Health:Life:GroupTermLife",
        "Expenses:Health:Medical:Insurance",
        "Expenses:Health:Vision:Insurance",
        "Expenses:Home:Electricity",
        "Expenses:Home:Internet",
        "Expenses:Home:Phone",
        "Expenses:Home:Rent",
        "Expenses:Taxes:Y2020:US:CityNYC",
        "Expenses:Taxes:Y2020:US:Federal:PreTax401k",
        "Expenses:Taxes:Y2020:US:Medicare",
        "Expenses:Taxes:Y2020:US:SDI",
        "Expenses:Taxes:Y2020:US:SocSec",
        "Expenses:Taxes:Y2020:US:State",
        "Expenses:Taxes:Y2021:US:CityNYC",
        "Expenses:Taxes:Y2021:US:Federal:PreTax401k",
        "Expenses:Taxes:Y2021:US:Medicare",
        "Expenses:Taxes:Y2021:US:SDI",
        "Expenses:Taxes:Y2021:US:SocSec",
        "Expenses:Taxes:Y2021:US:State",
        "Expenses:Taxes:Y2022:US:CityNYC",
        "Expenses:Taxes:Y2022:US:Federal:PreTax401k",
        "Expenses:Taxes:Y2022:US:Medicare",
        "Expenses:Taxes:Y2022:US:SDI",
        "Expenses:Taxes:Y2022:US:SocSec",
        "Expenses:Taxes:Y2022:US:State",
        "Expenses:Transport:Tram",
        "Expenses:Vacation",
        "Income:US:Babble:GroupTermLife",
        "Income:US:Babble:Match401k",
        "Income:US:Babble:Salary",
        "Income:US:Babble:Vacation",
        "Income:US:ETrade:GLD:Dividend",
        "Income:US:ETrade:ITOT:Dividend",
        "Income:US:ETrade:PnL",
        "Income:US:ETrade:VEA:Dividend",
        "Income:US:ETrade:VHT:Dividend",
        "Income:US:Federal:PreTax401k",
        "Liabilities:AccountsPayable",
        "Liabilities:US:Chase:Slate",
    ]
    response = client.get("/account")
    assert response.status_code == 200
    assert response.json() == expected


def test_account():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    response = client.get("/account/Assets:US:Babble:Vacation")
    assert response.status_code == 200
    assert response.json()["name"] == "Assets:US:Babble:Vacation"
    assert response.json()["open"] == "2020-01-01"
    assert response.json()["close"] is None
    assert response.json()["balance"] == [
        {"units": {"number": -2, "currency": "VACHR"}, "cost": None}
    ]
    assert len(response.json()["transactions"]) == 56

    response = client.get("/account/Assets:US:Babble:Vacations")
    assert response.status_code == 404
