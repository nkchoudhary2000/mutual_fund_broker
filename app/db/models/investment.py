from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_name = Column(String, nullable=False)
    fund_family = Column(String, nullable=False)
    units = Column(Float, nullable=False)
    nav = Column(Float, nullable=False)
    invested_on = Column(DateTime, default=datetime.utcnow)

    # 👇 Relationship back to User
    user = relationship("User", back_populates="investments")
