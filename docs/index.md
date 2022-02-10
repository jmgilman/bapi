# Introduction

The Beancount API is an HTTP API built on [FastAPI][1] and provides programmatic
access to a [Beancount][2] ledger. It is [OpenAPI][3] compliant and provides
rich access to the data contained within a ledger.

## Usage

The quickest way to deploy the API is via a container:

```shell
docker run \
    -v $(pwd)/testing/static.beancount:/run/beancount/main.beancount \
    -p 8080:8080 \
    ghcr.io/jmgilman/bapi
```

It can then be queried:

```shell
curl http://localhost:8080/directive
```

The API provides several configuration options for securing access as well as
automatically fetching ledger files from remote sources. See the navigation to
left for more details.

## Reloading

By default, the beancount data is only loaded and parsed once. The result is
cached and reused across all future requests. However, the API runs a continuous
background task that checks with the configured storage provider to determine
if the underlying data has changed. If a change is detected, the cache is
invalidated and the data is reloaded.

This happens outside of the main request context to bring consistency to the
response times of requests, even when the cache gets invalidated. How often
this check occurs can be configured in the environment:

```shell
export BAPI_CACHE_INTERVAL=5 # Every 5 seconds (default)
```

The method used for detecting changes is dependent on the storage provider. See
the provider documentation for more information.

## Environment Variables

| Name                 | Default Value  | Description                                                           |
| -------------------- | -------------- | --------------------------------------------------------------------- |
| BAPI_ENTRYPOINT      | main.beancount | The filename of the beancount ledger.                                 |
| BAPI_WORK_DIR        | /tmp/bean      | The location to search for the beancount ledger file.                 |
| BAPI_CACHE_INTERVAL  | 5              | Seconds to wait before checking for data changes.                     |
| BAPI_AUTH            | none           | The authentication type to use for protecting endpoints.              |
| BAPI_STORAGE         | local          | The type of storage backend to use for fetching the beancount ledger. |
| BAPI_JWT__ALGORITHMS | RS256          | A comma separated list of algorithms allowed for encryption.          |
| BAPI_JWT__AUDIENCE   | None           | The expected `aud` field of the JWT.                                  |
| BAPI_JWT__JWKS       | None           | Fully-qualified URL to a JWKS endpoint for finding the public key.    |
| BAPI_JWT__ISSUER     | None           | The JWT issuer.                                                       |
| BAPI_REDIS__CACHED   | False          | Whether the loaded value is a pickle cache.                           |
| BAPI_REDIS__CHANNEL  | beancount      | Channel to listen to for reloads.                                     |
| BAPI_REDIS__HOST     | localhost      | The hostname of the Redis server.                                     |
| BAPI_REDIS__KEY      | beancount      | The Redis key to read.                                                |
| BAPI_REDIS__PASSWORD | ""             | The Redis server password.                                            |
| BAPI_REDIS__PORT     | 6379           | The Redis server port.                                                |
| BAPI_REDIS__SSL      | True           | Whether to enable SSL for the Redis connection or not.                |
| BAPI_S3__BUCKET      | ""             | The name of the S3 bucket to download to the work directory.          |

[1]: https://fastapi.tiangolo.com/
[2]: https://beancount.github.io/docs/index.html
[3]: https://www.openapis.org/
