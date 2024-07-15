import numpy as np
import pandas as pd
from ..utils.data_loader import df_assets

def count_assets():
    """
    Counts the size of the asset database.
    """
    asset_stats = len(df_assets)
    return {"asset database size": asset_stats}

def list_all_assets():
    """
    Retrieves a list of all assets.
    """
    return df_assets['NAME'].to_list()

def get_asset_by_name(asset_name: str):
    """
    Retrieves asset details by asset name.
    """
    asset_row = df_assets[df_assets['NAME'] == asset_name]
    if not asset_row.empty:
        asset_details = asset_row.iloc[0].replace({np.nan: None, np.inf: None, -np.inf: None}).to_dict()
        return asset_details
    return None

def get_users_from_asset(asset_name: str):
    """
    Retrieves all known users for an asset.
    """
    asset_row = df_assets[df_assets["NAME"] == asset_name]
    
    if not asset_row.empty:
        users = asset_row.iloc[0]["USERS"]
        
        # Check for NaN and convert to None
        if pd.isna(users) or isinstance(users, (int, float)) and np.isinf(users):
            users = None
        
        return {"asset": asset_name, "users": users}

    return None

def get_assets_by_user(user_name: str):
    """
    Retrieve a list of Assets where a specified User has logged in over the past 30 days.
    """
    # Filter the DataFrame to find assets containing the user
    filtered_df = df_assets[df_assets["USERS"].apply(lambda users: user_name in users)]

    if filtered_df.empty:
        return None

    # Extract the index values
    return filtered_df['NAME'].tolist()
