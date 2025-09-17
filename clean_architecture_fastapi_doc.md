Clean Architecture with FastAPI: Complete Tutorial & Implementation

---

# ProjectApp Structure

```
ProjectApp
  App
     application
        services
          login_service.py
          user_service.py
        validators
          user_validator.py
     core
        dependencies.py
        file_manager.py
        middlewares.py
        security.py
     domain
        dtos
           UserCreate.py
           UserLogin.py
           UserResponse.py
        entities
           User.py
        interfaces
           i_login_service.py
           i_user_service.py
     hubs
        chat_hub.py
     infrastructure
        db
          base.py
          models.py
        repositories
          base
              base_repository.py
          user_repository.py
          login_repository.py
        interfaces
          i_user_repository.py
          i_login_repository.py
     presentation
        chat_controller.py
        demo_controller.py
        login_controller.py
        notify_controller.py
        user_controller.py
        voucher_controller.py
     utilities
     main.py
     config.py
  .env
```

---

# 0) Prerequisites
- Python >= 3.11
- FastAPI
- SQLAlchemy 2.x (async)
- Pydantic v2
- passlib[bcrypt] for password hashing
- python-jose for JWT

---

# 1) Domain Layer

## DTOs

### UserCreate.py
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
```

### UserLogin.py
```python
from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str
```

### UserResponse.py
```python
from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
```

## Entities

### user.py
```python
from typing import Optional

class User:
    def __init__(self, id: int, username: str, hashed_password: str, email: Optional[str] = None):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
```

## Interfaces

### i_login_service.py
```python
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User
from app.domain.dtos.UserLogin import UserLogin

class ILoginService(ABC):

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        pass

    @abstractmethod
    async def login(self, login_data: UserLogin) -> Optional[str]:
        pass
```

### i_user_service.py
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import User
from app.domain.dtos.UserCreate import UserCreate

class IUserService(ABC):

    @abstractmethod
    async def create_user(self, user_data: UserCreate) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def list_users(self) -> List[User]:
        pass
```

---

# 2) Infrastructure Layer

## DB Base (async)
### base.py
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

## Models
### models.py
```python
from sqlalchemy import Column, Integer, String
from .base import Base

class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column("UserName", String(50), nullable=True)
    hashed_password = Column("Hashed_Password", String(100), nullable=True)
    email = Column("Email", String(50), nullable=True)
```

## Repository Interfaces
### i_login_repository.py
```python
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User

class ILoginRepository(ABC):

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        pass
```

### i_user_repository.py
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import User
from app.domain.dtos.UserCreate import UserCreate

class IUserRepository(ABC):

    @abstractmethod
    async def add_user(self, user_data: UserCreate) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def list_all_users(self) -> List[User]:
        pass
```

## Repositories
### login_repository.py
```python
from sqlalchemy import select
from app.infrastructure.db.base import async_session
from app.infrastructure.db.models import User as UserModel
from app.infrastructure.interfaces.i_login_repository import ILoginRepository
from app.domain.entities.user import User

class LoginRepository(ILoginRepository):

    async def get_user_by_username(self, username: str) -> User | None:
        async with async_session() as session:
            result = await session.execute(select(UserModel).where(UserModel.username == username))
            db_user = result.scalars().first()
            if not db_user:
                return None
            return User(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password, email=db_user.email)
```

### user_repository.py
```python
from typing import List
from sqlalchemy import select
from app.infrastructure.db.base import async_session
from app.infrastructure.db.models import User as UserModel
from app.infrastructure.interfaces.i_user_repository import IUserRepository
from app.domain.entities.user import User
from app.core.security import hash_password
from app.domain.dtos.UserCreate import UserCreate

class UserRepository(IUserRepository):

    async def add_user(self, user_data: UserCreate) -> User:
        async with async_session() as session:
            db_user = UserModel(username=user_data.username, hashed_password=hash_password(user_data.password), email=user_data.email)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return User(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password, email=db_user.email)

    async def get_by_id(self, user_id: int) -> User | None:
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
```

---

# 3) Core - Security and Dependencies

### security.py
```python
from datetime import datetime, timedelta
from typing import Dict
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: Dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or settings.JWT_ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

### dependencies.py
```python
from app.application.services.login_service import LoginService
from app.application.services.user_service import UserService
from app.infrastructure.repositories.login_repository import LoginRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.interfaces.i_login_repository import ILoginRepository
from app.infrastructure.interfaces.i_user_repository import IUserRepository

def get_login_service() -> LoginService:
    repo: ILoginRepository = LoginRepository()
    service = LoginService(repo)
    return service

def get_user_service() -> UserService:
    repo: IUserRepository = UserRepository()
    service = UserService(repo

