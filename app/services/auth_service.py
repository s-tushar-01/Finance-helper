from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.core.exceptions import AppException

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise AppException("Invalid credentials", status_code=401)
        if not verify_password(password, user.password_hash):
            raise AppException("Invalid credentials", status_code=401)
        
        access_token = create_access_token(subject=str(user.id), role=user.role)
        return {"access_token": access_token, "token_type": "bearer"}
