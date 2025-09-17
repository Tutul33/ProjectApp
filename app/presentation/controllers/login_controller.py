#login_controller.py
from fastapi import APIRouter, Depends, HTTPException
from app.domain.dtos.user.UserLogin import UserLogin
from app.application.services.login_service import LoginService
from app.core.dependencies import get_login_service
from app.utilities.response_utils import wrap_response

router = APIRouter()

@router.post("/login")
async def login_user(
    user_login: UserLogin,
    login_service: LoginService = Depends(get_login_service)
):
    result = await login_service.login(user_login)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Wrap response
    return wrap_response(data=result.model_dump())
