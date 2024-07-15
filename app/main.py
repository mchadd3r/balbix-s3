"""
Simple Balbix API for interacting with scheduled data exports.
"""

from fastapi import FastAPI, Depends, Path
import app.api_metadata
from app.utils import basic_auth
from .routers import assets, users, network, cves, software, tags, observers

app = FastAPI(
    title=app.api_metadata.title,
    description=app.api_metadata.description,
    version=app.api_metadata.version,
    openapi_tags=app.api_metadata.tags_metadata,
)

app.include_router(assets.router, tags=["Assets"])
app.include_router(users.router, tags=["Users"])
app.include_router(network.router, tags=["Network"])
app.include_router(cves.router, tags=["CVEs"])
app.include_router(software.router, tags=["Software"])
app.include_router(tags.router, tags=["Tags"])
app.include_router(observers.router, tags=["Observers"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# @app.get(
#     "/users/list", responses={404: {"description": "Asset not found"}}, tags=["Users"]
# )
# def get_user_stats():
#     """
#     Retrieve a list of Observers and corresponding asset counts.
#     """
#     # Flatten the list of lists in the 'tags' column
#     users = [tag for tags_list in df_assets["USERS"] for tag in tags_list]
#     # Count the occurrences of each unique tag
#     counts = dict(Counter(users))
#     return counts


# # # # # # # # # # # # # # # #
# # Observer Endpoints
# # # # # # # # # # # # # # # #


# @app.get(
#     "/observers/stats",
#     responses={404: {"description": "Asset not found"}},
#     tags=["Observers"],
# )
# def get_observer_stats():
#     """
#     Retrieve a list of Observers and corresponding asset counts.
#     """
#     # Flatten the list of lists in the 'tags' column
#     observers = [tag for tags_list in df_assets["OBSERVERS"] for tag in tags_list]
#     # Count the occurrences of each unique tag
#     counts = dict(Counter(observers))
#     return counts


# @app.get(
#     "/observers/{name}",
#     responses={404: {"description": "Asset not found"}},
#     tags=["Observers"],
# )
# def get_asset_observers(name: str):
#     """
#     Retrieve a list of Observers for a given asset
#     """
#     if name not in df_assets.index:
#         raise HTTPException(status_code=404, detail="Asset not found")

#     item = df_assets.loc[name]

#     # Replace NaN and infinite values with None
#     item = item.replace({np.nan: None, np.inf: None, -np.inf: None})

#     return item.to_dict()


# # # # # # # # # # # # # # # #
# # CVE Endpoints
# # # # # # # # # # # # # # # #


# @app.get(
#     "/cve/stats", responses={404: {"description": "Asset not found"}}, tags=["CVEs"]
# )
# def get_cve_stats():
#     """
#     Retrieve stats about the CVE database.
#     """

#     return {"error": "Not yet implemented"}

# uvicorn app.main:app --reload
# run with uvicorn app:app --reload
# This will start the FastAPI server, and you can access the data at:

# http://127.0.0.1:8000/data to get all data
# http://127.0.0.1:8000/data/{item_id} to get data by ID (replace {item_id} with the actual ID)
