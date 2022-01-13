import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

try:
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASS"]
    server = os.environ["POSTGRES_SERVER"]
    port = os.environ["POSTGRES_PORT"]
    database = os.environ["POSTGRES_DB"]
except KeyError as e:
    exit(f"Missing required environment variable: {e.args[0]}")

url = f"postgresql://{user}:{password}@{server}:{port}/{database}"
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
