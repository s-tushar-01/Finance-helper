from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    data: Optional[T] = None
    message: Optional[str] = None
