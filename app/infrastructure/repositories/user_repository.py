from typing import List, Optional
from sqlalchemy import asc, desc, select
from app.infrastructure.db.base import async_session
from app.infrastructure.db.models.user import User as UserModel
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

    async def list_users(
        self, page: int, page_size: int, sort_field: str, ascending: bool
    ) -> dict:
        async with async_session() as session:
            # Sorting
            order_by = asc(getattr(UserModel, sort_field)) if ascending else desc(getattr(UserModel, sort_field))

            # Query with pagination
            stmt = select(UserModel).order_by(order_by).offset((page - 1) * page_size).limit(page_size)
            result = await session.execute(stmt)
            db_users = result.scalars().all()

            # Count total records
            total = (await session.execute(select(UserModel))).scalars().all()
            total_count = len(total)

            return {
                "total": total_count,
                "data": [
                    User(id=u.id, username=u.username, hashed_password=u.hashed_password, email=u.email)
                    for u in db_users
                ],
            }

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
