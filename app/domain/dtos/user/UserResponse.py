from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    username: str
    email: Optional[EmailStr] = None
    roleId: Optional[str] = None
    createDate: datetime
    isActive: bool
    roleName: Optional[str]
    model_config = {
        "from_attributes": True  # replaces orm_mode in Pydantic v1
    }
