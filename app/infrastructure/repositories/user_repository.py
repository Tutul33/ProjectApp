from typing import Optional
from sqlalchemy import asc, desc, func, select
from app.domain.entities.role import Role
from app.infrastructure.db.base import async_session
from app.infrastructure.db.models.user import User as UserModel
from app.infrastructure.db.models.role import Role as RoleModel
from app.infrastructure.interfaces.i_user_repository import IUserRepository
from app.domain.entities.user import User
from app.core.security import hash_password
import uuid

class UserRepository(IUserRepository):
    """Concrete repository for user management"""

    async def add_user(self, user_data: User) -> User:
         async with async_session() as session:
          new_id = str(uuid.uuid4())  # ✅ Generate GUID

          db_user = UserModel(
            id=new_id,   # assign GUID here
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
            email=user_data.email,
            roleId=user_data.roleId,
            isActive=user_data.isActive
          )
          session.add(db_user)
          await session.commit()
          await session.refresh(db_user)

          return User(
            id=db_user.id,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            email=db_user.email,
            roleId=db_user.roleId,
            createDate=db_user.createDate,
            isActive=db_user.isActive
          )
         
    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with async_session() as session:
            result = await session.execute(select(UserModel).where(UserModel.id == user_id))
            db_user = result.scalars().first()
            if not db_user:
                return None
            return User(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password, email=db_user.email)

    async def list_users(self, page: int, page_size: int, sort_field: str, ascending: bool) -> dict:
      async with async_session() as session:
        # Sorting
        order_by = asc(getattr(UserModel, sort_field)) if ascending else desc(getattr(UserModel, sort_field))
        print("B4RolesWithUsers:")
        # Query with JOIN
        stmt = (
            select(UserModel, RoleModel.name.label("roleName"))
            .join(RoleModel, UserModel.roleId == RoleModel.id)
            .order_by(order_by)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await session.execute(stmt)
        rows = result.all()  # [(UserModel, roleName), ...]
        print("RolesWithUsers:",rows)
        # Count total
        total_stmt = select(func.count()).select_from(UserModel)
        total_result = await session.execute(total_stmt)
        total_count = total_result.scalar_one()
        print("WithUsersRoleName:",rows)
        # Convert to Domain Entities (including roleName)
        users = []
        for user_model, role_name in rows:
            users.append(
                User(
                    id=user_model.id,
                    username=user_model.username,
                    hashed_password=user_model.hashed_password,
                    email=user_model.email,
                    roleId=user_model.roleId,
                    createDate=user_model.createDate,
                    isActive=user_model.isActive,
                    roleName=role_name,  # ✅ Add role name here
                )
            )

        return {"total": total_count, "data": users}

    async def get_by_username_or_email(self, username: Optional[str] = None, email: Optional[str] = None) -> Optional[User]:
        async with async_session() as session:
            query = select(UserModel)

            if username and email:
                query = query.where((UserModel.username == username) | (UserModel.email == email))
            elif username:
                query = query.where(UserModel.username == username)
            elif email:
                query = query.where(UserModel.email == email)
            else:
                return None  # no input provided

            result = await session.execute(query)
            db_user = result.scalars().first()

            if not db_user:
                return None

            return User(
                id=db_user.id,
                username=db_user.username,
                hashed_password=db_user.hashed_password,
                email=db_user.email,
                roleId=db_user.roleId,
                createDate=db_user.createDate,
                isActive=db_user.isActive
            )
