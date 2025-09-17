#i_login_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User

class ILoginRepository(ABC):
    """Interface for login data access"""

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        pass
