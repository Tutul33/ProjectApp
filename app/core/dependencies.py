from app.application.services.login_service import LoginService
from app.application.services.user_service import UserService
from app.infrastructure.interfaces.i_user_repository import IUserRepository
from app.infrastructure.repositories.login_repository import LoginRepository
from app.infrastructure.interfaces.i_login_repository import ILoginRepository
from app.infrastructure.repositories.user_repository import UserRepository

def get_login_service() -> LoginService:
    repo: ILoginRepository = LoginRepository()
    service = LoginService(repo)
    return service
def get_user_service() -> UserService:
    repo: IUserRepository = UserRepository()
    service = UserService(repo)
    return service
