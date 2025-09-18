from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.middlewares.exception_handler import global_exception_handler
#from app.core.middlewares.response_middleware import ResponseWrapperMiddleware
from app.presentation.controllers import login_controller, role_controller, user_controller
from app.infrastructure.db.base import Base, engine
import logging
from app.config import settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan handler replaces deprecated on_event("startup") and on_event("shutdown").
    This runs at app startup and shutdown.
    """
    # Startup: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully.")
    
    # Yield control to the app
    yield
    
    # Shutdown: optional cleanup
    await engine.dispose()
    logger.info("Engine disposed on shutdown.")

# Create FastAPI app with lifespan
app = FastAPI(title="Fast API", lifespan=lifespan)

# Global exception handler
app.add_exception_handler(Exception, global_exception_handler) 

# Global middleware for response wrapping
#app.add_middleware(ResponseWrapperMiddleware)

# Health check or root endpoint
@app.get("/")
def root():
    return {"message": "Hello, FastAPI is running!"}

# Include routers
app.include_router(login_controller.router, prefix="/api/auth", tags=["Auth"])
app.include_router(user_controller.router, prefix="/api/user", tags=["User"])
app.include_router(role_controller.router, prefix="/api/role", tags=["Role"])
