# app/application/services/user_service.py
from typing import Any, Dict, Optional
from app.application.mappers.mapper_utils import map_list_to_dto, map_to_dto, map_to_entity
from app.domain.entities.user import User
from app.domain.dtos.user.UserCreate import UserCreate
from app.domain.dtos.user.UserResponse import UserResponse
from app.domain.interfaces.i_user_service import IUserService
from app.infrastructure.interfaces.i_user_repository import IUserRepository
from app.domain.exceptions.already_exist_exceptions import AlreadyExistsException

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
            raise AlreadyExistsException(f"Username or email already taken: {user_data.username}")
        
        # DTO → Domain Entity
        role_entity: User = map_to_entity(User, user_data)
        
        # Persist domain entity
        saved_user: User = await self.repo.add_user(role_entity)
        
        # Domain Entity → DTO
        return map_to_dto(UserResponse, saved_user)

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user: Optional[User] = await self.repo.get_by_id(user_id)
        return map_to_dto(UserResponse,user) if user else None

    async def list_users(
        self, page: int = 1, page_size: int = 10, sort_field: str = "name", ascending: bool = True
       ) -> Dict[str, Any]:
        """
        Returns paginated list of users
        """
        result = await self.repo.list_users(page, page_size, sort_field, ascending)
        print("Inservice",result)
        return {
            "total": result["total"],
            "data": map_list_to_dto(UserResponse, result["data"]),
            "page": page,
            "page_size": page_size
        }
