import bdantic

from bdantic import models
from fastapi import APIRouter, Depends, HTTPException, Query
from ..dependencies import get_beanfile
from ..internal.beancount import BeancountFile, QueryError

router = APIRouter(prefix="/query", tags=["query"])


@router.get(
    "/",
    response_model=models.QueryResult,
    summary="Query the beancount data using a BQL query string",
    response_description="A QueryResult containing results of the query",
)
def query(
    bql: str = Query("", description="The BQL query string"),
    beanfile: BeancountFile = Depends(get_beanfile),
):
    """Queries the underlying beancount data using a BQL query string."""
    try:
        return bdantic.parse_query(beanfile.query(bql))
    except QueryError as e:
        raise HTTPException(status_code=400, detail=str(e))
