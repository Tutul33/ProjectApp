#login_repository.py
from sqlalchemy import select
from app.infrastructure.db.base import async_session
from app.infrastructure.db.models import User as UserModel
from app.infrastructure.interfaces.i_login_repository import ILoginRepository
from app.domain.entities.user import User

class LoginRepository(ILoginRepository):
    """Concrete repository for login"""

    async def get_user_by_username(self, username: str) -> User | None:
        async with async_session() as session:
            result = await session.execute(select(UserModel).where(UserModel.username == username))
            db_user = result.scalars().first()
            if not db_user:
                return None
            return User(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password, email=db_user.email)

