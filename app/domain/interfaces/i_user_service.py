#i_user_service.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from app.domain.entities.user import User
from app.domain.dtos.user.UserCreate import UserCreate

class IUserService(ABC):
    """Interface for user-related business logic"""

    @abstractmethod
    async def create_user(self, user_data: UserCreate) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    # @abstractmethod
    # async def list_users(self) -> List[User]:
    #     pass
    @abstractmethod
    async def list_users( self, page: int = 1, page_size: int = 10, sort_field: str = "name", ascending: bool = True) -> Dict[str, any]:
        """Fetch all users."""
        pass
