# app/presentation/user_controller.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.domain.dtos.user.UserCreate import UserCreate
from app.application.services.user_service import UserService
from app.core.dependencies import get_user_service
from app.utilities.response_utils import wrap_response


router = APIRouter()

@router.post("/")
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    user = await user_service.create_user(user_data)
    return wrap_response(data=user)

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Fetch a user by ID"""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return wrap_response(data=user)


@router.get("/")
async def list_users(user_service: UserService = Depends(get_user_service)):
    """Fetch all users"""
    user =  await user_service.list_users()
    return wrap_response(data=user)

