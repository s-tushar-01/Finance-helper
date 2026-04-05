from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    
    amount = Column(Float, nullable=False) # Must be > 0 (handled via validation/service)
    type = Column(String(20), nullable=False) # Stored as string from TransactionTypeEnum
    date = Column(DateTime, nullable=False, index=True)
    notes = Column(String(255), nullable=True, index=True) # Searchable
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    category = relationship("Category")
