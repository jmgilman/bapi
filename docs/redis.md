# Redis Configuration

The API can be configured to automatically fetch the contents of the ledger
file from a Redis database. This is a faster alternative to S3 and also offers
the advantage of being able to store a pickled cache to load from.

## Configuration

To enable Redis integration set the following environment variable:

```shell
export BAPI_STORAGE="redis"
```

Additionally, you must configure the connection details to the Redis server:

```shell
export BAPI_REDIS__HOST="my.redis.com"
export BAPI_REDIS__PORT=12345
export BAPI_REDIS__PASSWORD="supersecret"
export BAPI_REDIS__SSL=1 # Defaults to 1 (enable SSL)
```

Then, configure the Redis key from which the API will fetch from:

```shell
export BAPI_REDIS__KEY="mykey"
```

Upon startup, the API will connect to the configured Redis server and pull the
contents of the given key. The contents should be the full plain-text ledger
contents that can be given to the Beancount loader. This will be parsed and used
to populate the API data.

## Notifications

The API runs a background task that frequently checks in with the configured
storage provider to determine if the underlying data has changed. By default,
the data is only loaded once during startup and is then cached. The storage
provider informs the API when the underlying data changes so that the cache can
be invalidated and the data reloaded.

This is accomplished in Redis using a pubsub channel:

```shell
export BAPI_REDIS__CHANNEL="beancount"
```

When *any* message is received in the configured channel, the cache will be
invalidated and the data reloaded from the configured Redis key. It's
recommended to include publishing to this channel when you update the contents
of the Redis key in order to force a reload. See the example section below for
what this might look like.

## Cached

The contents of the key can alternatively be configured to be a pickle cache.
A large portion of the startup time of the container is consumed by the
beancount parser. This is especially true for large ledgers. The Redis key can
be populated with a LZMA compressed pickled version of a `BeancountFile`
instance. The `bdantic` package provides a method for accomplishing this:
`BeancountFile.compress()`. It's recommended to automatically run a script
whenever you make changes to your ledger files which can update the Redis key.
See the example section below for what this might look like.

To inform the API that the key is a cache, set the following:

```shell
export BAPI_REDIS__CACHED=1
```

When the server starts it will pull the token and unpickle the contents,
bypassing the need to run the beancount parser and dramatically improving the
startup time. While the benefits of this might seem low if the container is
always running, in models

## Example Script

```python
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
```

[1]: https://github.com/beancount/beancount/blob/master/beancount/loader.py
