from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.api.deps import require_viewer, require_admin
from app.schemas.category import CategoryCreate, CategoryOut
from app.services.category_service import CategoryService
from app.schemas.common import ResponseModel

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=ResponseModel[list[CategoryOut]])
def get_categories(db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    categories = CategoryService.get_categories(db, current_user.id)
    return ResponseModel(data=categories)

@router.post("", response_model=ResponseModel[CategoryOut], status_code=status.HTTP_201_CREATED)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    category = CategoryService.create_category(db, category_in, current_user.id)
    return ResponseModel(data=category, message="Category created")

@router.delete("/{category_id}", response_model=ResponseModel)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    CategoryService.delete_category(db, category_id, current_user.id)
    return ResponseModel(message="Category deleted")
