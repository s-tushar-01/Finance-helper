from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.core.exceptions import AppException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = security.decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise AppException("Could not validate credentials", status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise AppException("Could not validate credentials or token expired", status_code=status.HTTP_401_UNAUTHORIZED)
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise AppException("User not found", status_code=status.HTTP_404_NOT_FOUND)
    return user

def require_roles(roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise AppException(f"Operation not permitted. Required roles: {roles}", status_code=status.HTTP_403_FORBIDDEN)
        return current_user
    return role_checker

def require_viewer(current_user: User = Depends(require_roles(["viewer", "analyst", "admin"]))):
    return current_user

def require_analyst(current_user: User = Depends(require_roles(["analyst", "admin"]))):
    return current_user

def require_admin(current_user: User = Depends(require_roles(["admin"]))):
    return current_user
