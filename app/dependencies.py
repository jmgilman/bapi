import os

from beancount import loader
from functools import lru_cache
from .internal.sql.db import SessionLocal
from .settings import settings


@lru_cache()
def get_entries():
    entries, _, _ = loader.load_file(
        os.path.join(settings.working_dir, settings.bean_file)
    )
    return entries


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
