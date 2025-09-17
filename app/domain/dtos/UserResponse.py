#UserResponse.py
from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None

    model_config = {
        "from_attributes": True  # replaces orm_mode in Pydantic v1
    }
