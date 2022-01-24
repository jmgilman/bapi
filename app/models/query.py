from pydantic import BaseModel
from typing import Any, Dict, List


class QueryColumn(BaseModel):
    name: str
    type: str


QueryHeader = List[QueryColumn]
QueryRow = Dict[str, Any]


class QueryResult(BaseModel):
    header: QueryHeader
    rows: List[QueryRow]


class QueryError(Exception):
    pass
