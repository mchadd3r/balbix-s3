import numpy as np
import pandas as pd
from ..utils.data_loader import df_cves
from typing import List, Dict, Any

def count_cves():
    """
    Counts the size of the asset database.
    """
    asset_stats = len(df_cves)
    return {"asset database size": asset_stats}

def list_all_cves(asset_name: str = None):
    """
    Retrieves CVE-IDs, optionally filtered by a specific asset name.
    """
    if asset_name:
        result = df_cves[df_cves['Name'] == asset_name]['CVE'].dropna().unique().tolist()
    else:
        result = df_cves['CVE'].dropna().unique().tolist()
    
    return result

def list_tactical_cves(asset_name: str = None):
    """
    Retrieves CVE-IDs, optionally filtered by a specific asset name.
    """
    if asset_name:
        result = df_cves[df_cves['Name'] == asset_name].dropna().to_dict(orient='records')
    else:
        result = df_cves.dropna().to_dict(orient='records')
    
    return result

def list_cve_details(cve_id: str = None) -> List[Dict[str, Any]]:
    """
    Retrieves CVE details by CVE-ID
    """
    if cve_id:
        result = df_cves[df_cves['CVE'] == cve_id].dropna().to_dict(orient='records')
    else:
        result = df_cves.dropna().to_dict(orient='records')
    
    return result
