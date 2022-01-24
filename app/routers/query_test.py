from functools import lru_cache
from ..dependencies import BeanFile, get_beanfile
from ..main import app
from fastapi.testclient import TestClient


@lru_cache
def override():
    return BeanFile("testing/static.beancount")


def test_query():
    client = TestClient(app)
    app.dependency_overrides[get_beanfile] = override

    query = "SELECT date, narration, account, position"
    response = client.get(f"/query?bql={query}")
    assert response.status_code == 200
    assert response.json()["header"] == [
        {"name": "date", "type": "date"},
        {"name": "narration", "type": "str"},
        {"name": "account", "type": "str"},
        {"name": "position", "type": "Position"},
    ]
    assert response.json()["rows"][0] == {
        "date": "2020-01-01",
        "narration": "Opening Balance for checking account",
        "account": "Assets:US:BofA:Checking",
        "position": {
            "units": {"number": 2845.77, "currency": "USD"},
            "cost": None,
        },
    }
