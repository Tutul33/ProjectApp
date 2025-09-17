#user_service.py
from typing import List, Optional
from app.domain.entities.user import User
from app.domain.dtos.UserCreate import UserCreate
from app.domain.interfaces.i_user_service import IUserService
from app.infrastructure.interfaces.i_user_repository import IUserRepository

class UserService(IUserService):
    """Concrete implementation of IUserService"""

    def __init__(self, user_repository: IUserRepository):
        self.repo = user_repository

    async def create_user(self, user_data: UserCreate) -> User:
        return await self.repo.add_user(user_data)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return await self.repo.get_by_id(user_id)

    async def list_users(self) -> List[User]:
        return await self.repo.list_all_users()
