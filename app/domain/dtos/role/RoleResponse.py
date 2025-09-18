# app/domain/dtos/role/RoleResponse.py
from pydantic import BaseModel

class RoleResponse(BaseModel):
    id: int
    name: str    
    isActive: bool

    model_config = {
        "from_attributes": True  # replaces orm_mode in Pydantic v1
    }
