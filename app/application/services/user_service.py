from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.db.base import async_session
from app.core.security import hash_password
from app.domain.dtos import UserCreate
from app.infrastructure.db.models import User

class UserService:
    async def register_user(self, user: UserCreate):
        async with async_session() as session:
            repo = UserRepository(session)

            # Check if username exists
            if await repo.get_by_username(user.username):
                return {"error": "Username already exists"}

            # Hash password and create user
            hashed_pwd = hash_password(user.password)
            new_user = User(
                username=user.username,
                hashed_password=hashed_pwd,
                email=user.email
            )
            created_user = await repo.add_user(new_user)
            return {
                "message": "User created successfully",
                "user_id": created_user.id,
                "username": created_user.username
            }
