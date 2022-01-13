from sqlalchemy.orm import Session

from . import models, schemas


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Type).offset(skip).limit(limit).all()


def get_budget(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Budget).offset(skip).limit(limit).all()
