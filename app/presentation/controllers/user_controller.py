# app/presentation/user_controller.py
from fastapi import APIRouter, Depends, HTTPException, Query
from app.domain.dtos.user.UserCreate import UserCreate
from app.application.services.user_service import UserService
from app.core.dependencies import get_user_service
from app.utilities.response_utils import wrap_response


router = APIRouter()

@router.post("/")
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    user = await user_service.create_user(user_data)
    return wrap_response(data=user)

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Fetch a user by ID"""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return wrap_response(data=user)


# @router.get("/")
# async def list_users(user_service: UserService = Depends(get_user_service)):
#     """Fetch all users"""
#     user =  await user_service.list_users()
#     return wrap_response(data=user)
@router.get("/")
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_field: str = Query("name", description="Field to sort by"),
    ascending: bool = Query(True, description="Sort ascending?"),
    user_service: UserService = Depends(get_user_service)
):
    """Fetch paginated users"""
    roles = await user_service.list_users(page, page_size, sort_field, ascending)
    return wrap_response(data=roles)


