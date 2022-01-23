from .dependencies import authenticated
from fastapi import FastAPI, Depends
from .internal.s3 import S3Loader
from os.path import exists
from .routers import account, balance, directive, transactions
from .settings import Auth, bean_file, Storage, settings

title = "Beancount API"
version = "0.0.1"
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
app.include_router(balance.router)
app.include_router(directive.router)
app.include_router(transactions.router)


@app.on_event("startup")
def startup():
    if settings.storage == Storage.s3:
        s3 = S3Loader(settings)
        s3.load()

    if not exists(bean_file):
        raise FileNotFoundError(
            f"Unable to locate beancount file at: {bean_file}"
        )
