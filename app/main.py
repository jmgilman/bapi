import asyncio

from .dependencies import authenticated
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from jmespath.exceptions import LexerError  # type: ignore
from .routers import account, directive, query
from .internal.settings import Auth, settings, CacheInvalidator

app = FastAPI(
    title="Beancount API",
    description="""
The Beancount API (bapi) provides an HTTP API for viewing data derived from a
Beancount ledger file. It aims to provide as much of the underlying data as
possible in responses in order to maximize integration with other platforms.
""",
    version="0.1.0",
    contact={"name": "Joshua Gilman", "email": "joshuagilman@gmail.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)


@app.on_event("startup")
async def startup():
    """Startup handler for configuring dependencies."""
    # Force caching on the beancount file
    settings.beanfile

    # Setup cache invalidator
    asyncio.create_task(CacheInvalidator().main())

    # Setup authentication
    if settings.auth != Auth.none:
        app.router.dependencies.append(Depends(authenticated))

    # Add routes
    app.include_router(account.router)
    app.include_router(directive.router)
    app.include_router(query.router)


# Exception handlers


@app.exception_handler(LexerError)
def jmespath_exception_handler(_, exc: LexerError):
    """Provides an exception handler for catching JMESPath exceptions."""
    return JSONResponse(
        status_code=422,
        content={
            "message": f"Error in JMESPath filter expression: {exc.message}",
            "expression": exc.expression,
            "column": exc.lex_position,
            "token": exc.token_value,
        },
    )
