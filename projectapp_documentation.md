# ProjectApp Clean Architecture Documentation

**Project Name:** ProjectApp\
**Architecture:** Clean Architecture\
**Framework:** FastAPI\
**Database:** SQL Server (via SQLAlchemy)\
**Authentication:** JWT\
**Password Hashing:** bcrypt (PassLib)

---

## 1. Project Structure Overview

```
ProjectApp
  App
     application
        services
        validators
     core
     domain
        dtos
        entities
        interfaces
     hubs
     infrastructure
        db
        repositories
        interfaces
     presentation
     utilities
     main.py
     config.py
  .env
```

### Explanation:

- **application**: Business logic, service layer.
- **core**: Utilities, middlewares, security, DI.
- **domain**: Entities, DTOs, and abstract interfaces.
- **hubs**: Real-time hubs (chat, notifications).
- **infrastructure**: DB models and repositories.
- **presentation**: API controllers (FastAPI routes).
- **utilities**: Helper functions.
- **main.py**: App entry point.
- **config.py**: App settings.
- **.env**: Environment variables.

---

## 2. Domain Layer

### 2.1 Entities (`domain/entities/User.py`)

```python
class User:
    def __init__(self, id: int, username: str, hashed_password: str, email: Optional[str] = None):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
```

**Explanation:**

- Represents the **core User object**.
- Contains only business data.

### 2.2 DTOs (`domain/dtos/UserCreate.py`)

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
```

**Explanation:**

- DTOs validate incoming API data.
- Separates transport data from domain entities.

### 2.3 Interfaces (`domain/interfaces/i_user_service.py`)

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

**Explanation:**

- Defines service contracts.
- Allows **loose coupling** between layers.

---

## 3. Application Layer

### 3.1 Services (`application/services/user_service.py`)

```python
from app.domain.interfaces.i_user_service import IUserService
from app.infrastructure.interfaces.i_user_repository import IUserRepository
from app.domain.entities.user import User
from app.domain.dtos.UserCreate import UserCreate

class UserService(IUserService):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate) -> User:
        return await self.repository.add_user(user_data)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.repository.get_by_id(user_id)

    async def list_users(self) -> list[User]:
        return await self.repository.list_all_users()
```

**Explanation:**

- Implements IUserService.
- Contains business logic.
- Delegates DB operations to repository.

### 3.2 Validators (`application/validators/user_validator.py`)

- Optional layer to validate business rules (e.g., unique email, password strength).

---

## 4. Infrastructure Layer

### 4.1 Database Models (`infrastructure/db/models.py`)

```python
from sqlalchemy import Column, Integer, String
from .base import Base

class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True)
    username = Column("UserName", String(50))
    hashed_password = Column("Hashed_Password", String(100))
    email = Column("Email", String(50))
```

**Explanation:**

- Maps domain entities to DB tables.
- SQLAlchemy ORM is used for async DB operations.

### 4.2 Repositories (`infrastructure/repositories/user_repository.py`)

```python
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
            db_user = UserModel(
                username=user_data.username,
                hashed_password=hash_password(user_data.password),
                email=user_data.email
            )
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return User(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password, email=db_user.email)

    async def get_by_id(self, user_id: int) -> User:
        async with async_session() as session:
            result = await session.execute(select(UserModel).where(UserModel.id == user_id))
            db_user = result.scalars().first()
            return None if not db_user else User(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password, email=db_user.email)

    async def list_all_users(self) -> list[User]:
        async with async_session() as session:
            result = await session.execute(select(UserModel))
            users = result.scalars().all()
            return [User(id=u.id, username=u.username, hashed_password=u.hashed_password, email=u.email) for u in users]
```

**Explanation:**

- Implements **IUserRepository**.
- Handles DB CRUD operations.
- Uses async SQLAlchemy session.

---

## 5. Core Layer

### 5.1 Security (`core/security.py`)

- Handles JWT and password hashing.
- Functions: `hash_password()`, `verify_password()`, `create_access_token()`.

### 5.2 Dependency Injection (`core/dependencies.py`)

```python
def get_user_service() -> UserService:
    repo: IUserRepository = UserRepository()
    service = UserService(repo)
    return service
```

- Provides service instances to controllers.
- Enables **decoupling** of controllers and service implementations.

---

## 6. Presentation Layer

### 6.1 User Controller (`presentation/user_controller.py`)

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.application.services.user_service import UserService
from app.core.dependencies import get_user_service
from app.domain.dtos.UserCreate import UserCreate
from app.domain.dtos.UserResponse import UserResponse

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    user = await user_service.create_user(user_data)
    return UserResponse(**user.__dict__)
```

**Explanation:**

- Defines API endpoints.
- Uses DI to get service instances.
- Converts entities to response DTOs.

---

## 7. Example Flow: Create User

1. Client POSTs `/users` with `username`, `password`, `email`.
2. `user_controller.create_user()` calls `UserService.create_user()`.
3. `UserService` calls `UserRepository.add_user()`.
4. Repository inserts user into DB and returns entity.
5. Controller converts entity to DTO and returns JSON.

---

This structure is scalable for Login, ChatHub, Voucher, and Notifications, following the same Clean Architecture principles.

