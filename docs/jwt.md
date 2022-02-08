# JWT Configuration

The API can be configured to protect all endpoints by requiring requests to
include a valid JWT token in the header. If the token fails validation all
requests will be rejected with a 403 error. Note that enabling authentication
wil enable it for all endpoints - there's not currently a way to individually
control authentication (PR's are welcome!).

## Configuration

To enable JWT authentication set the following environment variable:

```shell
export BAPI_AUTH="jwt"
```

The remaining configuration is dependent on your individual setup. The following
environment variables need to be configured:

```shell
export BAPI_JWT__ALGORITHMS="RS256" # Type of encryption algorithms allowed
export BAPI_JWT__AUDIENCE="https://my.api.io" # JWT audience
export BAPI_JWT__JWKS="https://domain.us.auth0.com/.well-known/jwks.json" # JWKS endpoint
export BAPI_JWT__ISSUER="https://domain.us.auth0.com/" # Token issuer
```

The above shows what a configuration might look like for an API being [protected
by Auth0][1].

[1]: https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
