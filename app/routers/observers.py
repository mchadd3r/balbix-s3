from fastapi import APIRouter, Depends, HTTPException, Query
from ..services.observer_service import *
from ..utils.auth import basic_auth

router = APIRouter()

@router.get("/observers/list")
def list_observers(username: str = Depends(basic_auth), observer_name: str = Query(None)):
    """
    Retrieves a list of all tags, optionally filtered by observer name.
    """
    result = get_assets_by_observer(observer_name)
    if not result:
        raise HTTPException(status_code=404, detail="No tags found.")
    return result