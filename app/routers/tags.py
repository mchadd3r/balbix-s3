from fastapi import APIRouter, Depends, HTTPException, Query
from ..services.tag_service import *
from ..utils.auth import basic_auth

router = APIRouter()

@router.get("/tags/list")
def list_tags(username: str = Depends(basic_auth), asset_name: str = Query(None)):
    """
    Retrieves a list of all tags, optionally filtered by asset name.
    """
    result = get_tags_list(asset_name)
    if not result:
        raise HTTPException(status_code=404, detail="No tags found.")
    return result