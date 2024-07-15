from fastapi import APIRouter, HTTPException, Depends
from app.services.network_service import *
from app.utils.auth import basic_auth

router = APIRouter()

@router.get("/network/{ip_address}")
def get_assets_by_ip_address(ip_address: str, username: str = Depends(basic_auth)):
    """
    Retrieve a list of Assets by IP address.
    """
    result = list_assets_by_ip(ip_address)
    if not result:
        raise HTTPException(status_code=404, detail="No results found.")
    return result

@router.get("/network/sites/{site_name}")
def get_assets_by_site_name(site_name: str, username: str = Depends(basic_auth)):
    """
    Retrieve a list of Assets by Site Name.
    """
    result = list_assets_by_site_name(site_name)
    if not result:
        raise HTTPException(status_code=404, detail="No results found.")
    return result
