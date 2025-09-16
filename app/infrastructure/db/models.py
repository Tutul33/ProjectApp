# app/infrastructure/db/models.py
from sqlalchemy import Column, Integer, String
from .base import Base

class User(Base):
    __tablename__ = "Users"   # must match SQL Server table name
    __table_args__ = {"schema": "dbo"}
    
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column("UserName", String(50), nullable=True)   # nvarchar(50)
    hashed_password = Column("Hashed_Password", String(100), nullable=True)  # nvarchar(100)
    email = Column("Email", String(50), nullable=True)  # nvarchar(50)
