from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    roleId: Optional[int] = None
    createDate: datetime
    isActive: bool

    model_config = {
        "from_attributes": True  # replaces orm_mode in Pydantic v1
    }
