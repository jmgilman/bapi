from .dependencies import authenticated
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from .internal.s3 import S3Loader
from jmespath.exceptions import LexerError  # type: ignore
from os.path import exists
from .routers import account, directive, query
from .settings import Auth, bean_file, Storage, settings

title = "Beancount API"
version = "0.1.0"
contact = {"name": "Joshua Gilman", "email": "joshuagilman@gmail.com"}
license_info = {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
description = """
The Beancount API (bapi) provides an HTTP API for viewing data derived from a
Beancount ledger file. It aims to provide as much of the underlying data as
possible in responses in order to maximize integration with other platforms.
"""

# Setup app
if settings.auth == Auth.jwt:
    app = FastAPI(
        title=title,
        description=description,
        version=version,
        contact=contact,
        license_info=license_info,
        dependencies=[Depends(authenticated)],
    )
else:
    app = FastAPI(
        title=title,
        description=description,
        version=version,
        contact=contact,
        license_info=license_info,
    )

# Add routes
app.include_router(account.router)
app.include_router(directive.router)
app.include_router(query.router)
# app.include_router(transactions.router)


@app.on_event("startup")
def startup():
    if settings.storage == Storage.s3:
        s3 = S3Loader(settings)
        s3.load()

    if not exists(bean_file):
        raise FileNotFoundError(
            f"Unable to locate beancount file at: {bean_file}"
        )


@app.exception_handler(LexerError)
async def unicorn_exception_handler(request: Request, exc: LexerError):
    return JSONResponse(
        status_code=422,
        content={
            "message": f"Error in JMESPath filter expression: {exc.message}",
            "expression": exc.expression,
            "column": exc.lex_position,
            "token": exc.token_value,
        },
    )
