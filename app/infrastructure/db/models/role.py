from sqlalchemy import Boolean, Column, Integer, String

from app.infrastructure.db.base import Base

class Role(Base):
    __tablename__ = "Roles"
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    isActive = Column("IsActive",Boolean, nullable=False,default=True) 