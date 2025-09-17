#i_login_service.py
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User
from app.domain.dtos.UserLogin import UserLogin

class ILoginService(ABC):
    """Interface for login business logic"""

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        pass

    @abstractmethod
    async def login(self, login_data: UserLogin) -> Optional[str]:
        pass
