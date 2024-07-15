from fastapi import APIRouter, Depends, HTTPException, Query, Path
from ..services.cve_service import *
from ..utils.auth import basic_auth

router = APIRouter()

@router.get("/cves/stats")
def get_cve_database_stats(username: str = Depends(basic_auth)):
    """
    Get CVE Database Stats.
    """
    return count_cves()

@router.get("/cves/list")
def get_cve_list(username: str = Depends(basic_auth), asset_name: str = Query(None)):
    """
    Retrieves a list of all CVE-IDs, optionally filtered by asset name.
    """
    result = list_all_cves(asset_name)
    if not result:
        raise HTTPException(status_code=404, detail="No CVE-IDs found.")
    return result

@router.get("/cves/tactical/{asset_name}")
def get_cve_list(username: str = Depends(basic_auth), asset_name: str = Path(..., description="The name of the asset")):
    """
    Retrieves a list of tactical CVE recommendations by asset.
    """
    result = list_tactical_cves(asset_name)
    if not result:
        raise HTTPException(status_code=404, detail="No CVE-IDs found.")
    return result

@router.get("/cves/tactical/{cve_id}", response_model=List[Dict[str, Any]])
def get_cve_details(username: str = Depends(basic_auth), cve_id: str = Path(..., description="The CVE ID")):
    """
    Retrieves CVE details by ID.
    """
    result = list_cve_details(cve_id)
    if not result:
        raise HTTPException(status_code=404, detail="No CVE-IDs found.")
    return result
