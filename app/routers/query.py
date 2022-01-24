from fastapi import APIRouter, Depends, HTTPException, Query
from ..dependencies import get_beanfile
from ..models.core import QueryError, QueryResult

router = APIRouter(prefix="/query", tags=["query"])


@router.get(
    "/",
    response_model=QueryResult,
    summary="Query the beancount data using a BQL query string",
    response_description="A QueryResult containing results of the query",
)
def query(
    bql: str = Query("", description="The BQL query string"),
    beanfile=Depends(get_beanfile),
):
    """Queries the underlying beancount data using a BQL query string."""
    try:
        return beanfile.query(bql)
    except QueryError as e:
        raise HTTPException(status_code=400, detail=str(e))
