# app/config.py
from pydantic_settings import BaseSettings
from datetime import timedelta
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # ==============================
    # App Settings
    # ==============================
    APP_NAME: str = "SonaliAPI"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000

    # ==============================
    # SQL Server
    # ==============================
    SQLSERVER_HOST: str = ""
    SQLSERVER_PORT: int = 0
    SQLSERVER_DB: str = ""
    SQLSERVER_USER: str = ""
    SQLSERVER_PASSWORD: str = ""
    SQLSERVER_DRIVER: str = "ODBC Driver 18 for SQL Server"

    # ==============================
    # MongoDB
    # ==============================
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "sonali_mongo"
    MONGO_USER: str = ""
    MONGO_PASSWORD: str = ""

    # ==============================
    # PostgreSQL
    # ==============================
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "sonali_postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""

    # ==============================
    # JWT / Security
    # ==============================
    JWT_SECRET_KEY: str = "your_super_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 day
    PASSWORD_SALT_ROUNDS: int = 12  # added

    # ==============================
    # Redis
    # ==============================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    # ==============================
    # Celery
    # ==============================
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"       # added
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"   # added

    # ==============================
    # Logging
    # ==============================
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "logs/app.log"

    # ==============================
    # File Uploads
    # ==============================
    UPLOAD_FOLDER: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # @property
    # def SQLSERVER_CONNECTION_STRING(self) -> str:
    #     # Async connection using aioodbc
    #     return (
    #     f"mssql+aioodbc://{self.SQLSERVER_USER}:{self.SQLSERVER_PASSWORD}"
    #     f"@{self.SQLSERVER_HOST}:{self.SQLSERVER_PORT}/{self.SQLSERVER_DB}"
    #     f"?driver={self.SQLSERVER_DRIVER}"
    #     )

    @property
    def SQLSERVER_CONNECTION_STRING(self) -> str:
        """
        Async connection string for SQL Server using aioodbc.
        Handles special characters in password and named instance.
        TrustServerCertificate=yes is added to bypass SSL certificate validation.
        """
        # password = quote_plus(self.SQLSERVER_PASSWORD)
        # host = self.SQLSERVER_HOST.replace("\\", "\\\\")
        # driver = quote_plus(self.SQLSERVER_DRIVER)
    
        # return (
        #     f"mssql+aioodbc://{self.SQLSERVER_USER}:{password}@{host}/{self.SQLSERVER_DB}"
        #     f"?driver={driver}&TrustServerCertificate=yes"
        # )
        
        # user = "sa"
        # password = quote_plus("Sli@2025#")  # URL-encode special characters
        # host = "DESKTOP-A3JE4DR\\SQLDEV"    # double backslash
        # db = "SonaliDB"
        # driver = quote_plus("ODBC Driver 18 for SQL Server")
        
        user = self.SQLSERVER_USER
        password = quote_plus(self.SQLSERVER_PASSWORD)  # handle special characters
        host = self.SQLSERVER_HOST
        db = self.SQLSERVER_DB
        driver = quote_plus(self.SQLSERVER_DRIVER)
        
        return (
           f"mssql+aioodbc://{user}:{password}@{host}/{db}"
           f"?driver={driver}&TrustServerCertificate=yes" 
        )
        
    @property
    def MONGO_URI(self) -> str:
        if self.MONGO_USER:
            return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"

    @property
    def JWT_ACCESS_TOKEN_EXPIRE(self) -> timedelta:
        return timedelta(minutes=self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)


settings = Settings()
