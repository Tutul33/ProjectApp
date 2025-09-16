# domain/entities/user.py
from typing import Optional
#from pydantic import BaseModel, EmailStr
#from utilities.password_utils import verify_password, hash_password

class User:
    """Domain entity for User"""

    def __init__(self, id: int, username: str, hashed_password: str, email: Optional[str] = None):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.email = email

    # def check_password(self, plain_password: str) -> bool:
    #     """Business rule: verify password"""
    #     return verify_password(plain_password, self.hashed_password)

    # @classmethod
    # def create(cls, username: str, plain_password: str, email: Optional[str] = None):
    #     """Factory method for creating new User with hashed password"""
    #     hashed = hash_password(plain_password)
    #     return cls(id=0, username=username, hashed_password=hashed, email=email)
