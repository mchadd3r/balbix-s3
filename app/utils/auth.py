from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Basic username/password authentication for POC purposes.
    """
    api_username = secrets.compare_digest(credentials.username, "balbix")
    api_password = secrets.compare_digest(credentials.password, "bxs3api")
    if not (api_username and api_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
