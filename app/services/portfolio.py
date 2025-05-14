from sqlalchemy.orm import Session
from app.db.models.investment import Investment
from app.schemas.investment import InvestmentCreate

def create_investment(db: Session, user_id: int, investment: InvestmentCreate):
    db_investment = Investment(
        user_id=user_id,
        scheme_name=investment.scheme_name,
        fund_family=investment.fund_family,
        units=investment.units,
        nav=investment.nav,
    )
    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)
    return db_investment

def get_user_portfolio(db: Session, user_id: int):
    return db.query(Investment).filter(Investment.user_id == user_id).all()
