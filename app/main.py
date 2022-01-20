import os

from fastapi import FastAPI
from .internal.s3 import S3Loader
from .routers import account, balance, directive, transactions
from .settings import settings

description = """
The Beancount API (bapi) provides an HTTP API for viewing data derived from a 
Beancount ledger file. It aims to provide as much of the underlying data as
possible in responses in order to maximize integration with other platforms. 
"""

app = FastAPI(
    title="Beancount API",
    description=description,
    version="0.0.1",
    contact={"name": "Joshua Gilman", "email": "joshuagilman@gmail.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)
app.include_router(account.router)
app.include_router(balance.router)
app.include_router(directive.router)
app.include_router(transactions.router)


@app.on_event("startup")
def startup():
    s3 = S3Loader(settings)
    s3.load()
