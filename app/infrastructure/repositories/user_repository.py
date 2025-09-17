from typing import List, Optional
from sqlalchemy import select
from app.infrastructure.db.base import async_session
from app.infrastructure.db.models.user import User as UserModel
from app.infrastructure.interfaces.i_user_repository import IUserRepository
from app.domain.entities.user import User
from app.core.security import hash_password
from app.domain.dtos.user.UserCreate import UserCreate

class UserRepository(IUserRepository):
    """Concrete repository for user management"""

    async def add_user(self, user_data: UserCreate) -> User:
        async with async_session() as session:
            print("Repo here")
            db_user = UserModel(
                username=user_data.username,
                hashed_password=hash_password(user_data.password),
                email=user_data.email,
                roleId=user_data.roleId,
                isActive=user_data.isActive
            )
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return User(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password, email=db_user.email,roleId=db_user.roleId,createDate=db_user.createDate,isActive=db_user.isActive)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with async_session() as session:
            result = await session.execute(select(UserModel).where(UserModel.id == user_id))
            db_user = result.scalars().first()
            if not db_user:
                return None
            return User(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password, email=db_user.email)

    async def list_all_users(self) -> List[User]:
        async with async_session() as session:
            result = await session.execute(select(UserModel))
            users = result.scalars().all()
            return [User(id=u.id, username=u.username, hashed_password=u.hashed_password, email=u.email) for u in users]
        
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
