# Introduction

The Beancount API is an HTTP API built on
[FastAPI](https://fastapi.tiangolo.com/) and provides programmatic access to a
[Beancount](https://beancount.github.io/docs/index.html) ledger. It is
[OpenAPI](https://www.openapis.org/) compliant (see [API](api.md)) and provides
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
