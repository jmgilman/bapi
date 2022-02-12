from fastapi import Request
from pydantic import BaseModel

import jwt

from ..base import BaseAuth, ValidationError


class JWTConfig(BaseModel):
    """Configuration class for configuring JWT authentication

    Attributes:
        algorithms: A comma separated list of approved algorithms to use
        audience: The API audience
        jwks: The URL to a JWKS endpoint for fetching keys
        issuer: The token issuer
    """

    algorithms: str = "RS256"
    audience: str = ""
    jwks: str = ""
    issuer: str = ""


class JWTAuth(BaseAuth):
    """Provides an interface for authenticating requests with JWT tokens."""

    def authenticate(self, request: Request) -> bool:
        assert self.settings.jwt is not None

        header: str = request.headers.get("Authorization", None)
        if not header:
            return False

        try:
            token: str = header.split("Bearer ")[1]
        except IndexError:
            return False

        signing_key = self.client().get_signing_key_from_jwt(token).key
        try:
            jwt.decode(
                token,
                signing_key,
                algorithms=self.settings.jwt.algorithms.split(", "),
                audience=self.settings.jwt.audience,
                issuer=self.settings.jwt.issuer,
            )
        except jwt.exceptions.DecodeError:
            return False

        return True

    def client(self) -> jwt.PyJWKClient:
        """Creates a new `PyJWKClient` instance.

        Returns:
            A configured `PyJWKClient` instance.
        """
        assert self.settings.jwt is not None
        return jwt.PyJWKClient(self.settings.jwt.jwks)

    @staticmethod
    def validate(settings) -> None:
        if settings.jwt is None:
            raise ValidationError("Must set environment variables for JWT")
        elif not settings.jwt.audience:
            raise ValidationError(
                "Must set the JWT audience environment variable"
            )
        elif not settings.jwt.jwks:
            raise ValidationError("Must set the JWT JWKS environment variable")
        elif not settings.jwt.issuer:
            raise ValidationError("Must set the issuer environment variable")
