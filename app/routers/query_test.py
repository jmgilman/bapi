from testing import common as c


def setup_module(_):
    c.setup()


def test_query():
    with c.client() as client:
        query = "SELECT date, narration, account, position"

        response = client.get(f"/query?bql={query}")
        assert response.status_code == 200
        assert response.json()["columns"] == [
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
                "ty": "Position",
                "units": {
                    "ty": "Amount",
                    "number": 2845.77,
                    "currency": "USD",
                },
                "cost": None,
            },
        }
