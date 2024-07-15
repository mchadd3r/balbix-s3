from collections import Counter
import numpy as np
import pandas as pd
from ..utils.data_loader import df_assets

def get_user_stats():
    """
    Retrieve a list of Users and corresponding asset counts.
    """
    # Flatten the list of lists in the 'USERS' column
    users = [user for user_list in df_assets["USERS"] for user in user_list]
    # Count the occurrences of each unique user
    counts = dict(Counter(users))
    return counts