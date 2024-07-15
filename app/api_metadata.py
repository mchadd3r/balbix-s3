title = "Balbix S3 API"

version = "1.0.0"

description = """
This API Server is intended for deployment alongside scheduled Asset and Vulnerability Exports from Balbix. 

It provides a way for Balbix customers to programmatically interact with Assets, their corresponding attributes, and vulnerabilities without relying on a live connection to Balbix.
"""

tags_metadata = [
    {
        "name": "Assets",
        "description": "Assets contain a wide variety of attributes describing the type and location of devices discovered by Balbix.",
        "x-displayName": "Assets",
        "x-tagGroups": [{"name": "Assets", "tags": ["Assets"]}],
        "x-codeSamples": [
            {
                "lang": "Python",
                "label": "Python Request",
                "source": """
import requests

response = requests.get("http://127.0.0.1:8000/assets/Alice")
print(response.json())
""",
            }
        ],
    },
    {
        "name": "Users",
        "description": "Query Balbix to discover which assets your users interact with and their associated risks.",
        "x-displayName": "Users",
        "x-tagGroups": [{"name": "Users", "tags": ["Users"]}],
        "x-codeSamples": [
            {
                "lang": "Curl",
                "label": "Curl Request",
                "source": """
curl http://127.0.0.1:8000/
""",
            }
        ],
    },
    {
        "name": "Network",
        "description": "Query Balbix for Assets by Network attributes.",
        "x-displayName": "Network",
        "x-tagGroups": [{"name": "Network", "tags": ["Network"]}],
        "x-codeSamples": [
            {
                "lang": "Curl",
                "label": "Curl Request",
                "source": """
curl http://127.0.0.1:8000/
""",
            }
        ],
    },
    {
        "name": "Observers",
        "description": "Query Balbix to discover how Assets are being discovered and assess control coverage.",
        "x-displayName": "Observers",
        "x-tagGroups": [{"name": "Observers", "tags": ["Observers"]}],
        "x-codeSamples": [
            {
                "lang": "Curl",
                "label": "Curl Request",
                "source": """
curl http://127.0.0.1:8000/
""",
            }
        ],
    },
]
