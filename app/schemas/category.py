from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Groceries"
                }
            ]
        }
    }

class CategoryOut(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
