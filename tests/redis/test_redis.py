import json

import requests  # type: ignore


def test_redis(app_url, parsed_data):
    resp = requests.get(f"{app_url}/file").json()
    assert resp == json.loads(parsed_data.json())
