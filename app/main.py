import os

from fastapi import FastAPI
from .internal import s3
from .routers import account, balance, directive, transactions
from .settings import settings

description = """
The Finance API (fapi) provides access to personal financial data stored across
various platforms.

The API currently aggregates the following:

* Data scraped from the configured Beancount file
* Budget data stored in a PostgreSQL database

In most cases the data is simply presented as-is with little modification on
the server side. In other cases an endpoint may produce valid Beancount syntax
in order to automate certain tedious processes associated with a text-based
ledger system.
"""

app = FastAPI(
    title="Finance API",
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
def fetch_data():
    s3.download_all(settings.bucket, settings.working_dir)
