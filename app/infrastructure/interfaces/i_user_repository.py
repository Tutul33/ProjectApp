#i_user_prepository
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from app.domain.entities.user import User

class IUserRepository(ABC):
    """Interface for user data access"""

    @abstractmethod
    async def add_user(self, user_data: User) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass
   
    @abstractmethod
    async def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        """Get a user by username or email (for duplicate checking)."""
        pass
    
    @abstractmethod
    async def list_users( self, page: int = 1, page_size: int = 10, sort_field: str = "username", ascending: bool = True) -> Dict[str, any]:
        """Fetch all users."""
        pass

