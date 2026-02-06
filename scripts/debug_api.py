import requests
import json

GROUP_ID = "bd0500f1-1d71-4c8e-9e66-ccdcd32470c4" # From screenshot
URL = f"http://localhost:8000/api/v1/groups/{GROUP_ID}/participants"

payload = {
    "name": "Debug User",
    "phone": "+919999999999"
}

try:
    print(f"Sending POST to {URL}...")
    response = requests.post(URL, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request Failed: {e}")
