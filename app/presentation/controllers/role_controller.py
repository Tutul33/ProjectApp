# app/presentation/user_controller.py
from fastapi import APIRouter, Depends, HTTPException, Query
from app.domain.dtos.role.RoleCreate import RoleCreate
from app.application.services.role_service import RoleService
from app.core.dependencies import get_role_service
from app.utilities.response_utils import wrap_response


router = APIRouter()

@router.post("/")
async def create_role(
    role_data: RoleCreate,
    role_service: RoleService = Depends(get_role_service)
):
    """Create a new role"""
    role = await role_service.create_role(role_data)
    return wrap_response(data=role)

@router.get("/{role_id}")
async def get_user(
    role_id: int,
    role_service: RoleService = Depends(get_role_service)
):
    """Fetch a role by ID"""
    role = await role_service.get_user_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return wrap_response(data=role)

@router.get("/")
async def list_roles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_field: str = Query("name", description="Field to sort by"),
    ascending: bool = Query(True, description="Sort ascending?"),
    role_service: RoleService = Depends(get_role_service)
):
    """Fetch paginated roles"""
    roles = await role_service.list_roles(page, page_size, sort_field, ascending)
    return wrap_response(data=roles)
