from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.role import Role

class IRoleRepository(ABC):
    """Interface for role data access"""

    @abstractmethod
    async def add_role(self, role_entity: Role) -> Role:
        """Add a new role to the database and return the domain entity."""
        pass

    @abstractmethod
    async def get_by_id(self, role_id: int) -> Optional[Role]:
        """Fetch a role by ID."""
        pass

    @abstractmethod
    async def list_all_roles(self) -> List[Role]:
        """Fetch all roles."""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Role]:
        """Get a role by name (for duplicate checking)."""
        pass
