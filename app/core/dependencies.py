# app/core/dependencies.py
from app.core.di_container import container
from app.application.services.login_service import LoginService
from app.application.services.user_service import UserService
from app.application.services.role_service import RoleService

def get_login_service() -> LoginService:
    return container.resolve(LoginService)

def get_user_service() -> UserService:
    return container.resolve(UserService)

def get_role_service() -> RoleService:
    return container.resolve(RoleService)
