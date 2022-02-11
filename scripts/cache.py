import os
import redis
import sys

from beancount import loader
from bdantic import models


def main():
    if len(sys.argv) < 2:
        print("Please specify the path to the beancount file to cache")
        return

    file = sys.argv[1]
    if not os.path.exists(file):
        print(f"No file found at: {file}")
        return

    host = os.getenv("BAPI_REDIS__HOST", "localhost")
    port = os.getenv("BAPI_REDIS__PORT", 6379)
    password = os.getenv("BAPI_REDIS__PASSWORD", "")
    key = os.getenv("BAPI_REDIS__KEY", "beancount")
    chan = os.getenv("BAPI_REDIS__CHANNEL", "beancount")
    ssl = os.getenv("BAPI_REDIS__SSL", True)

    r = redis.Redis(
        host=host,
        port=int(port),
        password=password,
        ssl=bool(ssl),
    )

    data = models.BeancountFile.parse(loader.load_file(file)).compress()
    r.set(key, data)
    r.publish(chan, "update")


if __name__ == "__main__":
    main()
