from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Budget(Base):
    __tablename__ = "budget"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    gid = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
    tid = Column(Integer, ForeignKey("types.id"))
    type = relationship("Type")
    aid = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account")
    amount = Column(Float)
    created_at = Column(Date)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
