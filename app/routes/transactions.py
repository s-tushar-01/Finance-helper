from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.models.user import User
from app.api.deps import require_viewer, require_admin
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from app.services.transaction_service import TransactionService
from app.schemas.common import ResponseModel

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("", response_model=ResponseModel[TransactionOut], status_code=status.HTTP_201_CREATED)
def create_transaction(txn_in: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    txn = TransactionService.create_transaction(db, txn_in, current_user.id)
    return ResponseModel(data=txn, message="Transaction created")

@router.get("", response_model=ResponseModel[list[TransactionOut]])
def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    type: Optional[str] = None,
    category_id: Optional[int] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    search: Optional[str] = None,
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2000, le=2100),
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_viewer)
):
    txns = TransactionService.get_transactions(
        db, current_user.id, skip, limit, type, category_id, 
        min_amount, max_amount, search, month, year
    )
    return ResponseModel(data=txns)

@router.get("/{txn_id}", response_model=ResponseModel[TransactionOut])
def get_transaction(txn_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    txn = TransactionService.get_transaction(db, txn_id, current_user.id)
    return ResponseModel(data=txn)

@router.put("/{txn_id}", response_model=ResponseModel[TransactionOut])
def update_transaction(txn_id: int, txn_in: TransactionUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    txn = TransactionService.update_transaction(db, txn_id, txn_in, current_user.id)
    return ResponseModel(data=txn, message="Transaction updated")

@router.delete("/{txn_id}", response_model=ResponseModel)
def delete_transaction(txn_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    TransactionService.delete_transaction(db, txn_id, current_user.id)
    return ResponseModel(message="Transaction deleted")
