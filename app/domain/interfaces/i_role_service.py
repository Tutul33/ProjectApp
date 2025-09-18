#i_user_service.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.role import Role
from app.domain.dtos.role.RoleCreate import RoleCreate

class IRoleService(ABC):
    """Interface for user-related business logic"""

    @abstractmethod
    async def create_role(self, role_data: RoleCreate) -> Role:
        pass

    @abstractmethod
    async def get_role_by_id(self, role_id: int) -> Optional[Role]:
        pass

    @abstractmethod
    async def list_roles(self) -> List[Role]:
        pass
