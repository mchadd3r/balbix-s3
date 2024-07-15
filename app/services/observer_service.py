from collections import Counter
import numpy as np
import pandas as pd
from ..utils.data_loader import df_assets

def get_assets_by_observer(observer_name: str):
    """
    Retrieve a list of assets matching the observer name.
    """
    # Filter the DataFrame to find assets with the specified observer
    df_filtered = df_assets[df_assets['OBSERVERS'].apply(
        lambda observers: observer_name in observers if observers else False
    )]

    if df_filtered.empty:
        return None

    # Extract the index values (ASSET NAMES)
    return df_filtered['NAME'].tolist()