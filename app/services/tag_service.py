from collections import Counter
import numpy as np
import pandas as pd
from ..utils.data_loader import df_assets

def get_tags_list(asset_name: str = None):
    """
    Retrieve a list of tags, optionally filtered by asset name.
    """
    df_filtered = df_assets

    if asset_name:
        df_filtered = df_filtered[df_filtered["NAME"] == asset_name]

    # Extract individual tags from lists in the TAGS column
    tags = df_filtered['TAGS'].dropna().explode().unique().tolist()
    
    return tags