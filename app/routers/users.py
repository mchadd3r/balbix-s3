from fastapi import APIRouter, Depends, HTTPException
from ..services.user_service import *
from ..utils.auth import basic_auth

router = APIRouter()

@router.get("/users/list")
def list_user_stats(username: str = Depends(basic_auth)):
    """
    Retrieves a list of all users and corresponding asset count.
    """
    result = get_user_stats()
    if not result:
        raise HTTPException(status_code=404, detail="No users found.")
    return result