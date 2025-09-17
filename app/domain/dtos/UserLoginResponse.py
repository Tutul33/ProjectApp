# app/domain/dtos/UserLoginResponse.py
from pydantic import BaseModel
from typing import Optional
from app.domain.dtos.UserResponse import UserResponse

class UserLoginResponse(BaseModel):
    user: UserResponse
    token: str
