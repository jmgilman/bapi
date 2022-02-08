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

## Cached

The contents of the key can alternatively be configured to be a pickle cache.
A large portion of the startup time of the container is consumed by the
beancount parser. This is especially true for large ledgers. The Redis key can
be populated with a pickled version of the `(entries, errors, options)` tuple
that is returned by most of the [loader functions][1]. Once this is done,
simply inform the API:

```shell
export BAPI_REDIS__CACHED=1
```

When the server starts it will pull the token and unpickle the contents,
bypassing the need to run the beancount parser and dramatically improving the
startup time. While the benefits of this might seem low if the container is
always running, in models

[1]: https://github.com/beancount/beancount/blob/master/beancount/loader.py
