from fastapi import APIRouter

from app.api.v1 import account, directive, file, query

router = APIRouter()
router.include_router(account.router, prefix="/account", tags=["account"])
router.include_router(
    directive.router, prefix="/directive", tags=["directive"]
)
router.include_router(file.router, prefix="/file", tags=["file"])
router.include_router(query.router, prefix="/query", tags=["query"])
