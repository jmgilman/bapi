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
automatically fetching ledger files from remote sources. See the [docs][4] for
more in-depth usage and configuration information.

## Endpoints

| Endpoint     | Description
| ------------ | --------------------------------------------------------------------------------- |
| /account     | Fetch, list, and realize all accounts in the ledger                               |
| /directive   | Fetch all directives by type or generate Beancount syntax for each directive type |
| /query       | Fetch the results of querying the Beancount data using a BQL query                |
| /realize     | Performs a realization against the ledger                                         |

[1]: https://fastapi.tiangolo.com/
[2]: https://beancount.github.io/docs/index.html
[3]: https://www.openapis.org/
[4]: https://jmgilman.github.io/bapi/
