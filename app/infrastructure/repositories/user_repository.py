from sqlalchemy import select
from app.infrastructure.db.models import User  # SQLAlchemy model

class UserRepository:
    def __init__(self, session):
        self.session = session
        self.model = User

    async def get_by_username(self, username: str):
        result = await self.session.execute(
            select(self.model).where(self.model.username == username)
        )
        return result.scalars().first()

    async def add_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
