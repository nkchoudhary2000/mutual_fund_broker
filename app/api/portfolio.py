from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.investment import InvestmentCreate, InvestmentRead
from app.services import portfolio
from app.core.auth import get_current_user, get_db
from app.db.models.user import User
from typing import List

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.post("/", response_model=InvestmentRead)
def add_investment(investment: InvestmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return portfolio.create_investment(db, current_user.id, investment)

@router.get("/", response_model=List[InvestmentRead])
def view_portfolio(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return portfolio.get_user_portfolio(db, current_user.id)
