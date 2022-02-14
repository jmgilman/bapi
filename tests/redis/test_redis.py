import json
import os
import time

import requests  # type: ignore
from bdantic import models
from beancount import loader
from testcontainers.compose import DockerCompose  # type: ignore


def test_redis():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    no_pickle_path = os.path.join(cur_dir, ".env.no-pickle")
    pickle_path = os.path.join(cur_dir, ".env.pickle")

    # Test plain cache
    with DockerCompose(
        os.path.dirname(os.path.realpath(__file__)), env_file=no_pickle_path
    ) as comp:
        gen_host = comp.get_service_host("generator", 8001)
        gen_port = comp.get_service_port("generator", 8001)
        gen_url = f"http://{gen_host}:{gen_port}"

        bapi_host = comp.get_service_host("bapi", 8000)
        bapi_port = comp.get_service_port("bapi", 8000)
        bapi_url = f"http://{bapi_host}:{bapi_port}"

        # Wait for bapi to start
        wait_for_server(bapi_url)

        # Fetch the test ledger contents
        contents = requests.get(gen_url).text
        bf = models.BeancountFile.parse(loader.load_string(contents))

        # Test data was fetched from the Redis backend
        resp = requests.get(f"{bapi_url}/v1/file").json()
        assert resp == json.loads(bf.json())

    # Test pickled cache
    with DockerCompose(
        os.path.dirname(os.path.realpath(__file__)), env_file=pickle_path
    ) as comp:
        gen_host = comp.get_service_host("generator", 8001)
        gen_port = comp.get_service_port("generator", 8001)
        gen_url = f"http://{gen_host}:{gen_port}"

        bapi_host = comp.get_service_host("bapi", 8000)
        bapi_port = comp.get_service_port("bapi", 8000)
        bapi_url = f"http://{bapi_host}:{bapi_port}"

        # Wait for bapi to start
        wait_for_server(bapi_url)

        # Fetch the test ledger contents
        contents = requests.get(gen_url).text
        bf = models.BeancountFile.parse(loader.load_string(contents))

        # Test data was fetched from the Redis backend
        resp = requests.get(f"{bapi_url}/v1/file").json()
        assert resp == json.loads(bf.json())


def wait_for_server(url: str):
    for _ in range(5):
        try:
            requests.get(url, timeout=2)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(2)
            continue
