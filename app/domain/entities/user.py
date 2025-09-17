# domain/entities/user.py
from typing import Optional

class User:
    """Domain entity for a User"""
    def __init__(self, id: int, username: str, hashed_password: str, email: Optional[str] = None):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.email = email

