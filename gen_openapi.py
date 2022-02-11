"""
A script for generating an openapi.json file for use in mkdocs.
"""

import json

from app.main import app
from app.routers import account, directive, file, query, realize

if __name__ == "__main__":
    app.include_router(account.router)
    app.include_router(directive.router)
    app.include_router(file.router)
    app.include_router(query.router)
    app.include_router(realize.router)

    with open("docs/openapi.json", "w") as fd:
        json.dump(app.openapi(), fd)
