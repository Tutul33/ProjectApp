# app/presentation/user_controller.py
from fastapi import APIRouter, Depends, HTTPException
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
async def list_roles(role_service: RoleService = Depends(get_role_service)):
    """Fetch all roles"""
    role =  await role_service.list_roles()
    return wrap_response(data=role)

