from typing import List, Optional
from app.application.mappers.mapper_utils import map_to_dto, map_to_entity, map_list_to_dto
from app.domain.dtos.role.RoleCreate import RoleCreate
from app.domain.dtos.role.RoleResponse import RoleResponse
from app.domain.entities.role import Role
from app.domain.interfaces.i_role_service import IRoleService
from app.infrastructure.interfaces.i_role_repository import IRoleRepository
from app.domain.exceptions.already_exist_exceptions import AlreadyExistsException

class RoleService(IRoleService):
    """Concrete implementation of IRoleService"""

    def __init__(self, role_repository: IRoleRepository):
        self.repo = role_repository

    async def create_role(self, role_data: RoleCreate) -> RoleResponse:
        # Check for duplicates
        existing = await self.repo.get_by_name(role_data.name)
        if existing:
            raise AlreadyExistsException(f"Role Name already taken: {role_data.name}")

        # DTO → Domain Entity
        role_entity: Role = map_to_entity(Role, role_data)

        # Persist domain entity
        saved_role: Role = await self.repo.add_role(role_entity)

        # Domain Entity → DTO
        return map_to_dto(RoleResponse, saved_role)

    async def get_role_by_id(self, role_id: int) -> Optional[RoleResponse]:
        role_entity: Optional[Role] = await self.repo.get_by_id(role_id)
        return map_to_dto(RoleResponse, role_entity) if role_entity else None

    async def list_roles(self) -> List[RoleResponse]:
        roles: List[Role] = await self.repo.list_all_roles()
        return map_list_to_dto(RoleResponse, roles)
