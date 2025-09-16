from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.db.base import async_session
from app.core.security import verify_password

class LoginService:
    async def authenticate_user(self, username: str, password: str):
        async with async_session() as session:
            repo = UserRepository(session)
            user = await repo.get_by_username(username)
            if not user or not verify_password(password, user.hashed_password):
                return None
            return user
