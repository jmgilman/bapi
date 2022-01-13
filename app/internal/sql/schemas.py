from datetime import datetime
from pydantic import BaseModel


class Account(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Type(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Budget(BaseModel):
    id: int
    name: str
    category: Category
    type: Type
    account: Account
    amount: float
    created_at: datetime

    class Config:
        orm_mode = True
