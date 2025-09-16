from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# SQLAlchemy declarative base
Base = declarative_base()

# Async engine
engine = create_async_engine(
    settings.SQLSERVER_CONNECTION_STRING,  # Make sure connection string uses async driver
    echo=True
)

# Async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
