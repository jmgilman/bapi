import datetime
from beancount.core import amount, data
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

Flag = str


class Amount(BaseModel):
    number: float
    currency: str

    @staticmethod
    def from_bean(amt: amount.Amount):
        if amt is None:
            return None
        return Amount(number=float(amt.number), currency=amt.currency)


class Cost(BaseModel):
    number: float
    currency: str
    date: datetime.date
    label: str = ""

    @staticmethod
    def from_bean(cst: data.Cost):
        if cst is None:
            return None
        return Cost(
            number=float(cst.number),
            currency=cst.currency,
            date=cst.date,
            label=cst.label,
        )


class CostSpec(BaseModel):
    number_per: float = 0.0
    number_total: float = 0.0
    currency: str = ""
    date: datetime.date = None
    label: str = ""
    merge: bool = False

    @staticmethod
    def from_bean(cstspec: data.CostSpec):
        if cstspec is None:
            return None
        return CostSpec(
            number_per=float(cstspec.number_per),
            number_total=float(cstspec.number_total),
            currency=cstspec.currency,
            date=cstspec.date,
            label=cstspec.label,
            merge=cstspec.merge,
        )


class Posting(BaseModel):
    account: str
    units: Amount
    cost: Union[Cost, CostSpec] = None
    price: Amount = None
    flag: Flag = None
    meta: Dict[str, str] = {}

    @staticmethod
    def from_bean(post: data.Posting):
        if post is None:
            return None
        if isinstance(post.cost, data.Cost):
            cost = Cost.from_bean(post.cost)
        elif isinstance(post.cost, data.CostSpec):
            cost = CostSpec.from_bean(post.cost)
        else:
            cost = None

        return Posting(
            account=post.account,
            units=Amount.from_bean(post.units),
            cost=cost,
            price=Amount.from_bean(post.price),
            flag=post.flag,
            meta=post.meta,
        )


class Transaction(BaseModel):
    flag: Flag
    payee: Optional[str] = None
    narration: str
    tags: List[str] = []
    links: List[str] = []
    postings: List[Posting]

    @staticmethod
    def from_bean(tran: data.Transaction):
        if tran is None:
            return None

        postings = []
        for p in tran.postings:
            postings.append(Posting.from_bean(p))

        return Transaction(
            flag=tran.flag,
            payee=tran.payee,
            narration=tran.narration,
            tags=tran.tags,
            links=tran.links,
            postings=postings,
        )


class Account(BaseModel):
    name: str
    balance: Amount
    open: datetime.date
    close: Optional[datetime.date] = None
    transactions: List[Transaction]
