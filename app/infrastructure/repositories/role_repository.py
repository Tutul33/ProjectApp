from typing import List, Optional
from sqlalchemy import select
from app.infrastructure.db.base import async_session
from app.infrastructure.db.models.role import Role as RoleModel
from app.infrastructure.interfaces.i_role_repository import IRoleRepository
from app.domain.entities.role import Role

class RoleRepository(IRoleRepository):
    """Concrete repository for role management"""

    async def add_role(self, role_entity: Role) -> Role:
        async with async_session() as session:
            # Domain Entity → DB Model
            db_role = RoleModel(**role_entity.__dict__)
            db_role.id=None # Ensure SQLAlchemy does not try to insert an ID for auto increment
            session.add(db_role)
            await session.commit()
            await session.refresh(db_role)

            # DB Model → Domain Entity
            return Role(id=db_role.id, name=db_role.name, isActive=db_role.isActive)

    async def get_by_id(self, role_id: int) -> Optional[Role]:
        async with async_session() as session:
            result = await session.execute(select(RoleModel).where(RoleModel.id == role_id))
            db_role = result.scalars().first()
            if not db_role:
                return None
            return Role(id=db_role.id, name=db_role.name, isActive=db_role.isActive)

    async def list_all_roles(self) -> List[Role]:
        async with async_session() as session:
            result = await session.execute(select(RoleModel))
            db_roles = result.scalars().all()
            return [Role(id=r.id, name=r.name, isActive=r.isActive) for r in db_roles]

    async def get_by_name(self, name: str) -> Optional[Role]:
        async with async_session() as session:
            result = await session.execute(select(RoleModel).where(RoleModel.name == name))
            db_role = result.scalars().first()
            if not db_role:
                return None
            return Role(id=db_role.id, name=db_role.name, isActive=db_role.isActive)
