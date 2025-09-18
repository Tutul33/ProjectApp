from typing import List
from app.domain.entities.role import Role
from app.domain.dtos.role.RoleResponse import RoleResponse

def entity_to_response(role: Role) -> RoleResponse:
    """Map a single User entity to UserResponse DTO"""
    return RoleResponse(
        id=role.id,
        name=role.name,
        isActive=role.isActive
    )

def entities_to_responses(roles: List[Role]) -> List[RoleResponse]:
    """Map a list of Role entities to a list of RoleResponse DTOs"""
    return [entity_to_response(r) for r in roles]
