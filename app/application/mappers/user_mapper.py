from typing import List
from app.domain.entities.user import User
from app.domain.dtos.UserResponse import UserResponse

def entity_to_response(user: User) -> UserResponse:
    """Map a single User entity to UserResponse DTO"""
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        roleId=user.roleId,
        createDate=user.createDate,
        isActive=user.isActive
    )

def entities_to_responses(users: List[User]) -> List[UserResponse]:
    """Map a list of User entities to a list of UserResponse DTOs"""
    return [entity_to_response(u) for u in users]
