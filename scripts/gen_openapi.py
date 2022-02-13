"""
A script for generating an openapi.json file for use in mkdocs.
"""

import json

from app.api.v1 import api
from app.main import app

if __name__ == "__main__":
    app.include_router(api.router)

    with open("../docs/openapi.json", "w") as fd:
        json.dump(app.openapi(), fd)
