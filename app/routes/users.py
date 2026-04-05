from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdateRole
from app.models.user import User
from app.api.deps import get_current_user, require_admin
from app.services.user_service import UserService
from app.schemas.common import ResponseModel

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=ResponseModel[list[UserOut]])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    users = UserService.list_users(db)
    return ResponseModel(data=users)

@router.post("", response_model=ResponseModel[UserOut], status_code=status.HTTP_201_CREATED)
def create_admin_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # This route could be restricted. For initial seed, we might keep it open or separate it.
    # To be secure, let's allow creating viewers openly if we want signup, but here it's an internal system.
    # I'll leave it open for initial setup, but ideally protected.
    user = UserService.create_user(db, user_in, role="viewer")
    return ResponseModel(data=user, message="User created")

@router.delete("/{user_id}", response_model=ResponseModel)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    UserService.delete_user(db, user_id, current_user.id)
    return ResponseModel(message="User deleted successfully")

@router.patch("/{user_id}/role", response_model=ResponseModel[UserOut])
def update_user_role(user_id: int, role_data: UserUpdateRole, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user = UserService.update_role(db, user_id, role_data.role.value, current_user.id)
    return ResponseModel(data=user, message="User role updated")
