from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional
from app.models.enums import TransactionTypeEnum

class TransactionBase(BaseModel):
    category_id: Optional[int] = None
    amount: float = Field(gt=0, description="Amount must be greater than zero")
    type: TransactionTypeEnum
    date: datetime
    notes: Optional[str] = Field(None, max_length=255)

class TransactionCreate(TransactionBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "category_id": 1,
                    "amount": 150.75,
                    "type": "expense",
                    "date": "2024-05-15T14:30:00Z",
                    "notes": "Weekly groceries"
                }
            ]
        }
    }

    @model_validator(mode='after')
    def check_date_not_far_future(self):
        if self.date.replace(tzinfo=None) > datetime.now().replace(tzinfo=None):
            pass # Currently accepting any date as per earlier logic
        return self

class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionTypeEnum] = None
    date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=255)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "amount": 200.00,
                    "notes": "Corrected amount for groceries"
                }
            ]
        }
    }

class TransactionOut(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
