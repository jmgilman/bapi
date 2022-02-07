import jwt

from .jwt import JWTAuth
from unittest import mock


@mock.patch("jwt.decode")
@mock.patch("app.internal.settings.Settings")
@mock.patch("fastapi.Request")
@mock.patch("app.internal.auth.jwt.JWTAuth.client")
def test_authenticate(client, request, settings, decode):
    jwk = mock.Mock(jwt.PyJWKClient)
    jwk_resp = mock.Mock(jwt.PyJWK)
    jwk_resp.key = "123abc"
    jwk.get_signing_key_from_jwt.return_value = jwk_resp
    client.return_value = jwk
    request.headers.get.return_value = "Bearer abc123"
    settings.jwt.algorithms = "alg1, alg2"
    settings.jwt.audience = "aud"
    settings.jwt.jwks = "https://jwks.com"
    settings.jwt.issuer = "test"

    jwtauth = JWTAuth(settings)
    result = jwtauth.authenticate(request)

    assert result is True
    jwk.get_signing_key_from_jwt.assert_called_once_with("abc123")
    decode.assert_called_once_with(
        "abc123",
        "123abc",
        algorithms=["alg1", "alg2"],
        audience="aud",
        issuer="test",
    )

    request.headers.get.return_value = "A bad header"
    result = jwtauth.authenticate(request)
    assert result is False

    request.headers.get.return_value = "Bearer abc123"
    decode.side_effect = jwt.exceptions.DecodeError("Failed")
    result = jwtauth.authenticate(request)
    assert result is False


@mock.patch("app.internal.settings.Settings")
@mock.patch("jwt.PyJWKClient")
def test_client(client, settings):
    settings.jwt.jwks = "https://jwks.com"
    jwtauth = JWTAuth(settings)
    jwtauth.client()

    client.assert_called_once_with("https://jwks.com")
