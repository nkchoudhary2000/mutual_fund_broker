from pydantic import BaseModel
from typing import List
from datetime import datetime

class InvestmentCreate(BaseModel):
    scheme_name: str
    fund_family: str
    units: float
    nav: float

class InvestmentRead(BaseModel):
    id: int
    scheme_name: str
    fund_family: str
    units: float
    nav: float
    invested_on: datetime

    class Config:
        from_attributes = True

