# Beancount API (bapi)

> An HTTP API for serving up data contained within a Beancount ledger file. 

The Beancount API is an HTTP API which provides programmatic access to data that
is derived from one or more Beancount ledger files. It's built using
[FastAPI](https://fastapi.tiangolo.com/) and therefore provides a full Swagger
UI for interacting with the endpoints at `/docs`. 

The API models are designed to mimic the models found within the core Beancount
package. It attempts to remain as transparent as possible in returning all
possible information about a given entry. 

The API is designed to be shipped and deployed via a container. For security
reasons, the Beancount ledger files are only loaded after the container is
already running and are not packaged with the container. Currently, the only
supported method for obtaining the ledger files is via Amazon S3.