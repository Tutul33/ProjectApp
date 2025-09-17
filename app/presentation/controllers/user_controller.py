#user_controller.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.domain.dtos.UserCreate import UserCreate
from app.domain.dtos.UserResponse import UserResponse
from app.application.services.user_service import UserService
from app.core.dependencies import get_user_service

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    user = await user_service.create_user(user_data)
    return UserResponse(**user.__dict__)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.__dict__)

@router.get("/", response_model=List[UserResponse])
async def list_users(user_service: UserService = Depends(get_user_service)):
    users = await user_service.list_users()
    return [UserResponse(**u.__dict__) for u in users]
