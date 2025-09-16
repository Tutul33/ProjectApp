from fastapi import APIRouter, HTTPException
from app.domain.dtos.UserLogin  import UserLogin
from app.application.services.login_service import LoginService

router = APIRouter(prefix="/api/auth", tags=["Auth"])
login_service = LoginService()

@router.post("/login")
async def login_user(user: UserLogin):
    auth_user = await login_service.authenticate_user(user.username, user.password)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful", "username": auth_user.username}
