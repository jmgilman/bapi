import os

import redis
import requests  # type: ignore
from bdantic import models
from beancount import loader
from loguru import logger


def main():
    hostname = os.environ["REDIS_HOST"]
    gen_host = os.environ["GEN_HOST"]
    gen_port = os.environ["GEN_PORT"]
    pickle = os.environ["PICKLE"]
    key = os.environ["KEY"]

    logger.info(f"Connecting to Redis host {hostname}")
    r = redis.Redis(
        host=hostname,
    )

    gen_url = f"http://{gen_host}:{gen_port}/"
    logger.info(f"Reading beancount file at {gen_url}")

    contents = requests.get(gen_url).text

    if int(pickle):
        logger.info(f"Writing pickled file contents to {key}")
        bf = models.BeancountFile.parse(loader.load_string(contents))
        r.set(key, bf.compress())
    else:
        logger.info(f"Writing file contents to {key}")
        r.set(key, contents)


if __name__ == "__main__":
    main()
