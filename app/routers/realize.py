from .. import dependencies as dep
from bdantic import models
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/realize", tags=["realize"])


@router.get(
    "/",
    response_model=models.RealAccount,
    summary="Perform a realization on the ledger contents.",
    response_description="RealAccount holding the results of the realizaiton.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def realize(
    beanfile: models.BeancountFile = Depends(dep.get_beanfile),
):
    return beanfile.realize()
