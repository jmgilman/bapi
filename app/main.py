import asyncio

from . import logging
from .dependencies import authenticated
from .routers import account, directive, file, query
from .internal.cache import Cache
from .internal.settings import Auth, Settings
from fastapi import FastAPI, Depends
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from jmespath.exceptions import LexerError  # type: ignore
from loguru import logger

# Create app
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

# Initialize logging
logging.init()


@app.on_event("startup")
async def startup():
    """Startup handler for configuring dependencies."""
    logger.info(f"{app.title} v{app.version} starting")

    # Retrieve settings and setup cache
    app.state.settings = Settings()
    app.state.cache = Cache(
        app.state.settings.get_storage(), app.state.settings.cache_interval
    )

    # Run cache background task
    logger.info(f"Using {app.state.settings.storage} storage backend")
    logger.info("Starting cache refresh task")
    asyncio.create_task(app.state.cache.background())

    # Setup authentication
    if app.state.settings.auth != Auth.none:
        logger.info(f"Configuring {app.state.settings.auth} authentication")
        app.router.dependencies.append(Depends(authenticated))

    # Add middleware
    app.add_middleware(GZipMiddleware)

    # Add routes
    logger.info("Configuring routes")
    app.include_router(account.router)
    app.include_router(directive.router)
    app.include_router(file.router)
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
