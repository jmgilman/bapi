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

The Beancount API is an HTTP API built using [FastAPI](https://fastapi.tiangolo.com/) and provides programmatic access to data that is derived from Beancount ledger files. See the [docs](https://jmgilman.github.io/bapi/) for more details.

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
curl http://localhost:8080/transaction
```

By default the API will look for the primary beancount file at `/run/beancount/main.beancount`. The directory it searches can be controlled by setting the `BAPI_WORKDIR` environment variable and the filename can be controlled by setting the `BAPI_ENTRYPOINT` environment variable.

## Endpoints

| Endpoint     | Description
| ------------ | --------------------------------------------------------------------------------- |
| /account     | Fetch list of accounts or individual account information                          |
| /balance     | Fetch all account balances or individual account balances                         |
| /directive   | Fetch all directives by type or generate Beancount syntax for each directive type |
| /query       | Fetch the results of querying the Beancount data using a BQL query                |
| /transaction | Fetch and/or filter all transactions                                              |

## Storage

The API can be configured to pull files down from an Amazon S3 bucket into the
working directory before starting. The following environment variables must be set:

* **BAPI_STORAGE**: `s3`
* **BAPI_S3__BUCKET**: `bucket_name`

In addition to the above, the normal AWS environment variables must be set:

* **AWS_ACCESS_KEY_ID**
* **AWS_SECRET_ACCESS_KEY**
* **AWS_DEFAULT_REGION**

If configured correctly, all files in the specified S3 bucket will be downlaoded to the working directory before the server starts. This allows storing Beancount files remotely and only pulling them down when the container starts.

## Authentication

The API can be configured to protect all endpoints by validating that a valid
JWT is sent with each request. The following environment variables must be set:

* **BAPI_AUTH**: `jwt`
* **BAPI_JWT__ALGORITHMS**: Set to the algorithm used by incoming JWT's
* **BAPI_JWT__AUDIENCE**: The JWT audience
* **BAPI_JWT__JWKS**: The JWKS endpoint where the public key can be fetched
* **BAPI_JWT__ISSUER**: The JWT issuer

Once enabled, all endpoints will become protected and return a 403 if a valid JWT is not presented in the header.
