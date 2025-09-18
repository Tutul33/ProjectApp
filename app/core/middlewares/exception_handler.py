# app/core/middlewares/exception_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from app.utilities.common_response import APIResponse
from app.domain.exceptions.already_exist_exceptions import AlreadyExistsException
from fastapi import HTTPException

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, AlreadyExistsException):
        response = APIResponse(success=False, message="Already exists", errors=str(exc))
        return JSONResponse(status_code=400, content=response.model_dump())
    
    if isinstance(exc, HTTPException):
        response = APIResponse(success=False, message=exc.detail, errors=None)
        return JSONResponse(status_code=exc.status_code, content=response.model_dump())
    
    # handle unhandled exceptions
    response = APIResponse(success=False, message="Internal server error", errors=str(exc))
    return JSONResponse(status_code=500, content=response.model_dump())
