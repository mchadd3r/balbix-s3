from fastapi import APIRouter, Depends, HTTPException, Query
from ..services.software_service import *
from ..utils.auth import basic_auth

router = APIRouter()

@router.get("/software/list")
def list_software(username: str = Depends(basic_auth), asset_name: str = Query(None)):
    """
    Retrieves a list of all vulnerable software, optionally filtered by asset name.
    """
    result = get_software_list(asset_name)
    if not result:
        raise HTTPException(status_code=404, detail="No software found.")
    return result