from collections import Counter
import numpy as np
import pandas as pd
from ..utils.data_loader import df_cves

def get_software_list(asset_name: str = None):
    """
    Retrieve a list of vulnerable software, optionally filtered by asset name.
    """
    df_filtered = df_cves

    if asset_name:
        df_filtered = df_filtered[df_filtered['ASSET NAME'] == asset_name]

    software_list = df_filtered['SOFTWARE'].dropna().replace([np.inf, -np.inf], None).unique().tolist()
    return software_list