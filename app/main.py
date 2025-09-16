from fastapi import FastAPI
from app.presentation.controllers import login_controller, user_controller

app = FastAPI(title="Fast API")

# Health check or root endpoint
@app.get("/")
def root():
    return {"message": "Hello, FastAPI is running!"}

# Include routers
app.include_router(login_controller.router, prefix="/api/auth", tags=["Auth"])
app.include_router(user_controller.router, prefix="/api/user", tags=["User"])
