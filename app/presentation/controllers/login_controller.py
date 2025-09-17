#login_controller.py
from fastapi import APIRouter, Depends, HTTPException
from app.domain.dtos.UserLogin import UserLogin
from app.application.services.login_service import LoginService
from app.core.dependencies import get_login_service

router = APIRouter()

@router.post("/login")
async def login_user(
    user_login: UserLogin,
    login_service: LoginService = Depends(get_login_service)
):
    token = await login_service.login(user_login)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful", "access_token": token}
