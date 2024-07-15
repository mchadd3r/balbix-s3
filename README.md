# Balbix S3 API

A self-contained Python Application/FastAPI Server designed to make Asset and Vulnerability exports from Balbix more accessible within a broader ecosystem of tools.

Despite the name, this application is designed to run locally and within a secure environment; it does not contain any logic for Cloud deployment or basic essentials like SSL.

## Features / How to Use this Application

- Create a Python 3.10+ virtual environment and install dependencies from requirements.txt
- Upload .zip files taken from Balbix to the data folder; only Asset Exports and Tactical CVE Exports will be used
- Configure static credentials in `utils/auth.py`
- Run the application `uvicorn app.main:app --reload`
- Access the documentation for available endpoints via ReDoc at `http://localhost:8000/redoc`

## Caveats / Warranty
- This application code is provided as-is with no warranty and no support
- Your own exports from Balbix may vary; schema changes in the imported .zip files will result in failure to start unless those changes are handled within `balbix_data_loader.py`
- This application has not been stress tested but should handle processing of exports > 1 GB with ease
