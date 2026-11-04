
import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("XKDR_API_KEY")

if not API_KEY:
    raise ValueError("API key not found in .env")

# API endpoint
url = "https://airquality.xkdr.org/v1/meta"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Send API request
response = requests.get(
    url,
    headers=headers,
    timeout=30
)

print("Status Code:", response.status_code)

response.raise_for_status()

data = response.json()

print("\nAPI Connection Successful!")
print(data)
