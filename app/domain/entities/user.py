from typing import Optional
from datetime import datetime, timezone

class User:
    """Domain entity for a User"""

    def __init__(
        self,
        id: Optional[str]=None,
        username: Optional[str]=None,
        password:Optional[str]=None,
        hashed_password: Optional[str]=None,
        email: Optional[str] = None,
        roleId: Optional[int] = None,
        roleName: Optional[str] = None,
        createDate: Optional[datetime] = None,
        isActive: bool = True
    ):
        self.id = id
        self.username = username
        self.password = password
        self.hashed_password = hashed_password
        self.email = email
        self.roleId = roleId
        self.roleName = roleName
        self.createDate = createDate or datetime.now(timezone.utc)  # timezone-aware UTC
        self.isActive = isActive
