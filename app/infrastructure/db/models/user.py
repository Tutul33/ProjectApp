from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    id = Column(String(50), primary_key=True)
    username = Column("UserName", String(50), nullable=False)
    hashed_password = Column("Hashed_Password", String(100), nullable=False)
    email = Column("Email", String(50), nullable=True)
    roleId = Column("RoleId", String(50), ForeignKey("dbo.Roles.id"), nullable=False)
    createDate = Column("CreateDate", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    isActive = Column("IsActive", Boolean, nullable=False, default=True)

    # ORM relationship to Role
    role = relationship("Role", backref="users")
