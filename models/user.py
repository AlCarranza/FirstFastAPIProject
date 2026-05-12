# Extra: Use of pydantic
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    age: int = Field(gt=0)
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    password: Optional[int] = None