from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.services.auth_service import AuthService
from app.schemas.token import Token
from app.schemas.common import ResponseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Note: OAuth2 form uses 'username' field for email in this case if client sends it that way.
    # We will assume username field contains email based on common Swagger usage, or adjust:
    return AuthService.authenticate_user(db, email=form_data.username, password=form_data.password)
