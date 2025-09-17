from typing import List, Optional
from sqlalchemy import select
from app.infrastructure.db.base import async_session
from app.infrastructure.db.models import User as UserModel
from app.infrastructure.interfaces.i_user_repository import IUserRepository
from app.domain.entities.user import User
from app.core.security import hash_password
from app.domain.dtos.UserCreate import UserCreate

class UserRepository(IUserRepository):
    """Concrete repository for user management"""

    async def add_user(self, user_data: UserCreate) -> User:
        async with async_session() as session:
            db_user = UserModel(
                username=user_data.username,
                hashed_password=hash_password(user_data.password),
                email=user_data.email
            )
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return User(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password, email=db_user.email)

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
