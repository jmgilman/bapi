from .. import dependencies as dep
from bdantic import models
from fastapi import APIRouter, Depends, Query


router = APIRouter(prefix="/query", tags=["query"])


@router.get(
    "/",
    response_model=models.QueryResult,
    summary="Query the beancount data using a BQL query string.",
    response_description="A QueryResult containing results of the query.",
)
async def query(
    bql: str = Query("", description="The BQL query string"),
    beanfile: models.BeancountFile = Depends(dep.get_beanfile),
):
    return beanfile.query(bql)
