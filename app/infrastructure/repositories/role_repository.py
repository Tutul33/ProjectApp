from typing import Dict, List, Optional
from sqlalchemy import select
from app.infrastructure.db.base import async_session, get_collection
from app.infrastructure.db.models.role import Role as RoleModel
from app.infrastructure.interfaces.i_role_repository import IRoleRepository
from app.domain.entities.role import Role

#For Mongo Only
from bson import ObjectId

class RoleRepository(IRoleRepository):
    """Concrete repository for role management"""
    def __init__(self):
        self.collection = get_collection("roles")#For MongoDB Only
    """For MSSQL"""   
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
    
    """For MongoDB"""
    async def add_role(self, role_entity: Role) -> Role:
        """
        Domain Entity → MongoDB document
        """
        print("RoleRepositoryIn");
        doc = {
            "name": role_entity.name,
            "isActive": role_entity.isActive
        }
        result = await self.collection.insert_one(doc)
        print("Add Result:",result)
        return Role(id=str(doc["_id"]), name=role_entity.name, isActive=role_entity.isActive)

    async def get_by_id(self, role_id: str) -> Optional[Role]:
        doc = await self.collection.find_one({"_id": ObjectId(role_id)})
        if not doc:
            return None
        return Role(id=str(doc["_id"]), name=doc["name"], isActive=doc["isActive"])

    async def list_all_roles(self) -> List[Role]:
        cursor = self.collection.find()
        roles = []
        async for doc in cursor:
            roles.append(Role(id=str(doc["_id"]), name=doc["name"], isActive=doc["isActive"]))
        return roles

    async def get_by_name(self, name: str) -> Optional[Role]:
        doc = await self.collection.find_one({"name": name})
        if not doc:
            return None
        return Role(id=str(doc["_id"]), name=doc["name"], isActive=doc["isActive"])
    
    async def list_roles(
        self, page: int = 1, page_size: int = 10, sort_field: str = "name", ascending: bool = True
        ) -> Dict[str, any]:
        """
        Returns paginated roles with total count.

        :param page: Page number (1-based)
        :param page_size: Number of items per page
        :param sort_field: Field to sort by
        :param ascending: Sort order
        :return: dict with 'total' and 'data'
        """
        skip = (page - 1) * page_size
        sort_order = 1 if ascending else -1

        total = await self.collection.count_documents({})
        cursor = self.collection.find().sort(sort_field, sort_order).skip(skip).limit(page_size)

        roles: List[Role] = []
        async for doc in cursor:
            roles.append(Role(id=str(doc["_id"]), name=doc["name"], isActive=doc["isActive"]))
        #print("RolesNowInRepo:",roles)
        return {"total": total, "data": roles}
