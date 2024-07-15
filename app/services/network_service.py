import numpy as np
import pandas as pd
from ..utils.data_loader import df_assets

def list_assets_by_ip(ip_address: str):
    """
    Retrieve a list of Assets by IP address.
    """
    # Filter the DataFrame to find assets containing the IP address
    filtered_df = df_assets[df_assets["IP Addresses"].apply(lambda ip_addresses: ip_address in ip_addresses)]

    if filtered_df.empty:
        return None

    # Extract the index values
    return filtered_df['NAME'].tolist()

def list_assets_by_site_name(site_name: str):
    """
    Retrieve a list of Assets by Site Name.
    """
    # Filter the DataFrame to find assets with the site name
    filtered_df = df_assets[df_assets["SITE"].apply(lambda site: site is not None and site_name in site)]

    if filtered_df.empty:
        return None

    # Extract the index values
    return filtered_df['NAME'].tolist()