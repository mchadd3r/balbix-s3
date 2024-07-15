import pandas as pd
from app.utils import balbix_data_loader

# Load the asset dataframe
def load_asset_data():
    df_assets = pd.DataFrame()
    df_assets = balbix_data_loader.read_asset_file("./app/data/assets.zip")
    df_assets = balbix_data_loader.convert_asset_df(df_assets)
    # df_assets.set_index("NAME", inplace=True)
    return df_assets

df_assets = load_asset_data()

# # Load the CVE dataframe
# def load_cve_data():
#     df_cves = pd.DataFrame()
#     df_cves = balbix_data_loader.read_cve_file("./app/data/cves.zip")
#     df_cves = balbix_data_loader.convert_cve_df(df_cves)
#     return df_cves

# df_cves = load_cve_data()

# Load the tactical CVE dataframe
def load_tactical_cve_data():
    df_cves = pd.DataFrame()
    df_cves = balbix_data_loader.read_tactical_cve_file("./app/data/tactical.zip")
    df_cves = balbix_data_loader.convert_tactical_cve_df(df_cves)
    return df_cves

df_cves = load_tactical_cve_data()