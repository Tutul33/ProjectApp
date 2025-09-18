
#For MSSQL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
#For Mongo
from motor.motor_asyncio import AsyncIOMotorClient
#Settings
from app.config import settings

'''For MSSQL Start'''

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

'''For MSSQL END'''

'''For MONGODB Start'''

# Async MongoDB client
mongo_client = AsyncIOMotorClient(settings.MONGO_URI)

# Database reference
db = mongo_client[settings.MONGO_DB]

# Helper to get a collection
def get_collection(name: str):
    return db[name]

'''For MONGODB END'''
