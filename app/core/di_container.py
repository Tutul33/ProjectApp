# app/core/container.py
import punq

# Repositories
from app.infrastructure.repositories.login_repository import LoginRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.role_repository import RoleRepository

from app.infrastructure.interfaces.i_login_repository import ILoginRepository
from app.infrastructure.interfaces.i_user_repository import IUserRepository
from app.infrastructure.interfaces.i_role_repository import IRoleRepository

# Services
from app.application.services.login_service import LoginService
from app.application.services.user_service import UserService
from app.application.services.role_service import RoleService

# DI container
container = punq.Container()

# --- Register repositories ---
container.register(ILoginRepository, LoginRepository)
container.register(IUserRepository, UserRepository)
container.register(IRoleRepository, RoleRepository)

# --- Register services ---
container.register(LoginService, LoginService)
container.register(UserService, UserService)
container.register(RoleService, RoleService)
