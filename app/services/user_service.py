from sqlalchemy.orm import Session
from app.models.user import User
from app.models.category import Category
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.core.exceptions import AppException

class UserService:
    @staticmethod
    def create_user(db: Session, user_in: UserCreate, role: str = "viewer"):
        existing_user = db.query(User).filter(User.email == user_in.email).first()
        if existing_user:
            raise AppException("Email already registered", status_code=400)
            
        new_user = User(
            email=user_in.email,
            username=user_in.username,
            password_hash=get_password_hash(user_in.password),
            role=role
        )
        db.add(new_user)
        try:
            db.commit()
            db.refresh(new_user)
        except Exception:
            db.rollback()
            raise AppException("Failed to create user", status_code=500)
            
        # Add default categories
        defaults = ["Food", "Rent", "Salary", "Entertainment"]
        for cat_name in defaults:
            db.add(Category(user_id=new_user.id, name=cat_name))
        
        try:
            db.commit()
        except Exception:
            db.rollback()
            
        return new_user

    @staticmethod
    def list_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def delete_user(db: Session, user_id: int, current_admin_id: int):
        if user_id == current_admin_id:
            raise AppException("Admin cannot delete themselves", status_code=400)
            
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AppException("User not found", status_code=404)
            
        db.delete(user)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise AppException("Failed to delete user")

    @staticmethod
    def update_role(db: Session, user_id: int, role: str, current_admin_id: int):
        if user_id == current_admin_id:
            raise AppException("Admin cannot change their own role here", status_code=400)
            
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AppException("User not found", status_code=404)
            
        user.role = role
        try:
            db.commit()
            db.refresh(user)
            return user
        except Exception:
            db.rollback()
            raise AppException("Failed to update user role", status_code=500)
