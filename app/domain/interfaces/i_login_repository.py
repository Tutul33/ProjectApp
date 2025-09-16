# domain/interfaces/i_user_repository.py
from abc import ABC, abstractmethod
from domain.entities.user import User
from typing import Optional

class ILoginRepository(ABC):
    """Interface for Login repository"""

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def add(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass
