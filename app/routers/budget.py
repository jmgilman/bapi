from ..dependencies import get_db
from fastapi import APIRouter, Depends
from ..internal.sql import crud, schemas
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/budget/", response_model=List[schemas.Budget])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    budget = crud.get_budget(db, skip=skip, limit=limit)
    return budget


@router.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories
