# Beancount API (bapi)

<p align="center">
    <a href="https://github.com/jmgilman/bapi/actions/workflows/ci.yml">
        <img src="https://github.com/jmgilman/bapi/actions/workflows/ci.yml/badge.svg"/>
    </a>
    <a href="https://jmgilman.github.io/bapi/">
        <img src="https://img.shields.io/badge/docs-passing-brightgreen"/>
    </a>
</p>

> An HTTP API for serving up data contained within a Beancount ledger file.

The Beancount API is an HTTP API built using [FastAPI][1] and provides
programmatic access to data that is derived from Beancount ledger files. See
the [docs][2] for more details.

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

By default the API will look for the primary beancount file at
`/run/beancount/main.beancount`. The directory it searches can be controlled by
setting the `BAPI_WORKDIR` environment variable and the filename can be
controlled by setting the `BAPI_ENTRYPOINT` environment variable.

## Endpoints

| Endpoint     | Description
| ------------ | --------------------------------------------------------------------------------- |
| /account     | Fetch, list, and realize all accounts in the ledger                               |
| /directive   | Fetch all directives by type or generate Beancount syntax for each directive type |
| /query       | Fetch the results of querying the Beancount data using a BQL query                |

## Storage

The API can be configured to pull files down from various backends. Currently
this includes locally, loading a key from Redis, or downloading from an Amazon
S3 bucket. See the environment variables section below for more details.

* **BAPI_STORAGE**: `local` or `redis` or `s3`

Note that internally the API uses the `boto3` Python package for S3 which pulls
authentication details from various places. See the [documentation][3] for more
details.

The Redis client can be configured to pull a pickle cache instead of expecting
the raw contents of a Beancount ledger. In this case, the key is expected to
contain a pickled version of the `(entries, errors, options)` tuple that is
returned when the Beancount loader is called. This can greatly improve startup
speeds on large ledgers as it removes the need to parse it again.

## Authentication

The API can be configured to protect all endpoints through various
authentication schemes. Currently, the only supported scheme is JWT. See the
environment variables section below for more details.

* **BAPI_AUTH**: `none` or `jwt`

## Environment Variables

| Name                 | Default Value  | Description                                                           |
| -------------------- | -------------- | --------------------------------------------------------------------- |
| BAPI_ENTRYPOINT      | main.beancount | The filename of the beancount ledger.                                 |
| BAPI_WORK_DIR        | /tmp/bean      | The location to search for the beancount ledger file.                 |
| BAPI_AUTH            | none           | The authentication type to use for protecting endpoints.              |
| BAPI_STORAGE         | local          | The type of storage backend to use for fetching the beancount ledger. |
| BAPI_JWT__ALGORITHMS | RS256          | A comma separated list of algorithms allowed for encryption.          |
| BAPI_JWT__AUDIENCE   | None           | The expected `aud` field of the JWT.                                  |
| BAPI_JWT__JWKS       | None           | Fully-qualified URL to a JWKS endpoint for finding the public key.    |
| BAPI_JWT__ISSUER     | None           | The JWT issuer.                                                       |
| BAPI_REDIS__CACHED   | False          | Whether the loaded value is a pickle cache                            |
| BAPI_REDIS__HOST     | localhost      | The hostname of the Redis server                                      |
| BAPI_REDIS__KEY      | beancount      | The Redis key to read                                                 |
| BAPI_REDIS__PASSWORD | ""             | The Redis server password                                             |
| BAPI_REDIS__PORT     | 6379           | The Redis server port                                                 |
| BAPI_REDIS__SSL      | True           | Whether to enable SSL for the Redis connection or not                 |
| BAPI_S3__BUCKET      | ""             | The name of the S3 bucket to download to the work directory.          |

[1]: https://fastapi.tiangolo.com/
[2]: https://jmgilman.github.io/bapi/
[3]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#environment-variables
