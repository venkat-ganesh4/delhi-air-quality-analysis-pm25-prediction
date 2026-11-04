
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("XKDR_API_KEY")

url = "https://airquality.xkdr.org/v1/stations"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(url, headers=headers, timeout=30)

print("Status Code:", response.status_code)

response.raise_for_status()

data = response.json()

print("\nAvailable response keys:")
print(data.keys() if isinstance(data, dict) else type(data))

print("\nAPI Response:")
print(data)
