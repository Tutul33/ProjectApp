from fastapi import APIRouter
from app.domain.dtos.UserCreate  import UserCreate
from app.application.services.user_service import UserService

router = APIRouter()
user_service = UserService()  # Service manages DB internally

@router.post("/register")
async def register_user(user: UserCreate):
    return await user_service.register_user(user)
