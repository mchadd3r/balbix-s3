from fastapi import APIRouter, Depends, HTTPException
from ..services.asset_service import *
from ..utils.auth import basic_auth

router = APIRouter()

@router.get("/assets/stats")
def get_asset_database_stats(username: str = Depends(basic_auth)):
    """
    Get Asset Database Stats.
    """
    return count_assets()


@router.get("/assets/list")
def get_asset_list(username: str = Depends(basic_auth)):
    """
    List endpoint.
    """
    return list_all_assets()

@router.get("/assets/{asset_name}")
def get_asset_details(
    asset_name: str,
    username: str = Depends(basic_auth)
):
    """
    Retrieve asset details by name.
    """
    asset = get_asset_by_name(asset_name)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.get("/assets/{asset_name}/users")
def get_asset_users(
    asset_name: str,
    username: str = Depends(basic_auth)
):
    """
    Retrieve asset details by name.
    """
    users = get_users_from_asset(asset_name)
    if users is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return users

#TODO move to users
@router.get("/assets/user/{user_name}")
def get_assets_for_user(user_name: str, username: str = Depends(basic_auth)):
    """
    Retrieve a list of Assets where a specified User has logged in over the past 30 days.
    """
    result = get_assets_by_user(user_name)
    if not result:
        raise HTTPException(status_code=404, detail="User not found in any asset")
    return result