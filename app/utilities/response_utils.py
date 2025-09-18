# app/utilities/response_utils.py
from app.utilities.common_response import APIResponse

def wrap_response(data=None, message="Success", success=True, errors=None):
    return APIResponse(success=success, message=message, data=data, errors=errors).model_dump()

