from typing import Optional
from datetime import datetime, timezone

class User:
    """Domain entity for a User"""

    def __init__(
        self,
        id: int,
        username: str,
        hashed_password: str,
        email: Optional[str] = None,
        roleId: Optional[int] = None,
        createDate: Optional[datetime] = None,
        isActive: bool = True
    ):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
        self.roleId = roleId
        self.createDate = createDate or datetime.now(timezone.utc)  # timezone-aware UTC
        self.isActive = isActive
