from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    roleId: Optional[str] = None  # Optional role assignment
    isActive: bool = True          # Default active

    model_config = {
        "extra": "forbid"  # disallow extra fields in request
    }
