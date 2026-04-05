from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.enums import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "newuser@example.com",
                    "username": "johndoe",
                    "password": "strongpassword123"
                }
            ]
        }
    }

class UserUpdateRole(BaseModel):
    role: RoleEnum
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "role": "analyst"
                }
            ]
        }
    }

class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True
