import json

import requests  # type: ignore


def test_redis(app_url, parsed_data):
    # Test data was fetched from the Redis backend
    resp = requests.get(f"{app_url}/file").json()
    assert resp == json.loads(parsed_data.json())
