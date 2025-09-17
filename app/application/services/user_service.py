# app/application/services/user_service.py
from typing import List, Optional
from app.domain.entities.user import User
from app.domain.dtos.UserCreate import UserCreate
from app.domain.dtos.UserResponse import UserResponse
from app.domain.interfaces.i_user_service import IUserService
from app.infrastructure.interfaces.i_user_repository import IUserRepository
from app.application.mappers.user_mapper import entity_to_response, entities_to_responses
from app.domain.exceptions.user_exceptions import UserAlreadyExistsException

class UserService(IUserService):
    """Concrete implementation of IUserService"""

    def __init__(self, user_repository: IUserRepository):
        self.repo = user_repository

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        # Check for duplicates before adding
        existing = await self.repo.get_by_username_or_email(
            username=user_data.username,
            email=user_data.email
        )
        if existing:
            raise UserAlreadyExistsException(f"Username or email already taken: {user_data.username}")

        user: User = await self.repo.add_user(user_data)
        return entity_to_response(user)

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user: Optional[User] = await self.repo.get_by_id(user_id)
        return entity_to_response(user) if user else None

    async def list_users(self) -> List[UserResponse]:
        users: List[User] = await self.repo.list_all_users()
        return entities_to_responses(users)
