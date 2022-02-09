from bdantic import models
from fastapi import APIRouter, Depends, Query
from ..dependencies import get_beanfile

router = APIRouter(prefix="/query", tags=["query"])


@router.get(
    "/",
    response_model=models.QueryResult,
    summary="Query the beancount data using a BQL query string.",
    response_description="A QueryResult containing results of the query.",
)
def query(
    bql: str = Query("", description="The BQL query string"),
    beanfile: models.BeancountFile = Depends(get_beanfile),
):
    return beanfile.query(bql)
