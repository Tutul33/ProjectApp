#i_user_prepository
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import User
from app.domain.dtos.UserCreate import UserCreate

class IUserRepository(ABC):
    """Interface for user data access"""

    @abstractmethod
    async def add_user(self, user_data: UserCreate) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def list_all_users(self) -> List[User]:
        pass
    
    @abstractmethod
    async def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        """Get a user by username or email (for duplicate checking)."""
        pass

