from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.core.exceptions import AppException

class TransactionService:
    @staticmethod
    def create_transaction(db: Session, txn_in: TransactionCreate, user_id: int):
        if txn_in.category_id:
            cat = db.query(Category).filter(Category.id == txn_in.category_id, Category.user_id == user_id).first()
            if not cat:
                raise AppException("Invalid category id or not owned by user", status_code=400)
                
        new_txn = Transaction(
            user_id=user_id,
            category_id=txn_in.category_id,
            amount=txn_in.amount,
            type=txn_in.type.value,
            date=txn_in.date,
            notes=txn_in.notes
        )
        db.add(new_txn)
        try:
            db.commit()
            db.refresh(new_txn)
            return new_txn
        except Exception:
            db.rollback()
            raise AppException("Failed to create transaction", status_code=500)

    @staticmethod
    def get_transaction(db: Session, txn_id: int, user_id: int):
        txn = db.query(Transaction).filter(Transaction.id == txn_id, Transaction.user_id == user_id).first()
        if not txn:
            raise AppException("Transaction not found", status_code=404)
        return txn

    @staticmethod
    def get_transactions(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 20,
        txn_type: str = None,
        category_id: int = None,
        min_amount: float = None,
        max_amount: float = None,
        search: str = None,
        month: int = None,
        year: int = None
    ):
        if limit > 100:
            limit = 100
            
        query = db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if txn_type:
            query = query.filter(Transaction.type == txn_type)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
        if min_amount is not None:
            query = query.filter(Transaction.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Transaction.amount <= max_amount)
        
        if month:
            query = query.filter(extract('month', Transaction.date) == month)
        if year:
            query = query.filter(extract('year', Transaction.date) == year)
            
        if search and len(search) >= 2:
            search_pattern = f"%{search}%"
            # Join category if we want to search by category name
            query = query.outerjoin(Category)
            query = query.filter(
                (Transaction.notes.ilike(search_pattern)) | 
                (Category.name.ilike(search_pattern))
            )
            
        query = query.order_by(Transaction.date.desc())
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_transaction(db: Session, txn_id: int, txn_in: TransactionUpdate, user_id: int):
        txn = db.query(Transaction).filter(Transaction.id == txn_id, Transaction.user_id == user_id).first()
        if not txn:
            raise AppException("Transaction not found", status_code=404)
            
        if txn_in.category_id is not None:
            cat = db.query(Category).filter(Category.id == txn_in.category_id, Category.user_id == user_id).first()
            if not cat:
                raise AppException("Invalid category id or not owned by user", status_code=400)
            txn.category_id = txn_in.category_id
            
        if txn_in.amount is not None:
            txn.amount = txn_in.amount
        if txn_in.type is not None:
            txn.type = txn_in.type.value
        if txn_in.date is not None:
            txn.date = txn_in.date
        if txn_in.notes is not None:
            txn.notes = txn_in.notes
            
        try:
            db.commit()
            db.refresh(txn)
            return txn
        except Exception:
            db.rollback()
            raise AppException("Failed to update transaction", status_code=500)

    @staticmethod
    def delete_transaction(db: Session, txn_id: int, user_id: int):
        txn = db.query(Transaction).filter(Transaction.id == txn_id, Transaction.user_id == user_id).first()
        if not txn:
            raise AppException("Transaction not found", status_code=404)
            
        db.delete(txn)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise AppException("Failed to delete transaction", status_code=500)
