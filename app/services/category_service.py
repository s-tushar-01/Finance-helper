from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.core.exceptions import AppException

class CategoryService:
    @staticmethod
    def get_categories(db: Session, user_id: int):
        return db.query(Category).filter(Category.user_id == user_id).all()

    @staticmethod
    def create_category(db: Session, category_in: CategoryCreate, user_id: int):
        new_cat = Category(user_id=user_id, name=category_in.name)
        db.add(new_cat)
        try:
            db.commit()
            db.refresh(new_cat)
            return new_cat
        except IntegrityError:
            db.rollback()
            raise AppException("Category with this name already exists for this user", status_code=400)
        except Exception:
            db.rollback()
            raise AppException("Failed to create category", status_code=500)

    @staticmethod
    def delete_category(db: Session, category_id: int, user_id: int):
        cat = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
        if not cat:
            raise AppException("Category not found", status_code=404)
        
        db.delete(cat)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise AppException("Failed to delete category", status_code=500)
