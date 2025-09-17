#login_service.py
from typing import Optional
from app.domain.dtos.UserLoginResponse import UserLoginResponse
from app.domain.dtos.UserLogin import UserLogin
from app.domain.entities.user import User
from app.domain.interfaces.i_login_service import ILoginService
from app.infrastructure.interfaces.i_login_repository import ILoginRepository
from app.core.security import verify_password, create_access_token

class LoginService(ILoginService):
    """Concrete implementation of ILoginService"""

    def __init__(self, login_repository: ILoginRepository):
        self.login_repository = login_repository

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.login_repository.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def login(self, login_data: UserLogin) -> Optional[UserLoginResponse]:
        # Authenticate user
        user = await self.authenticate_user(
            login_data.username, login_data.password
        )
        if not user:
            return None

        # Create token
        token = create_access_token({"sub": user.username})

        # Return DTO
        return UserLoginResponse(user=user, token=token)
