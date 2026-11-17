from pydantic import BaseModel,EmailStr
from src.db.models import UserRole
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.CUSTOMER

class UserResponse(BaseModel):
    id:UUID
    email: EmailStr
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str