
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

params = {
    "state": "Delhi"
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

response.raise_for_status()

data = response.json()

# Handle the API response
if isinstance(data, list):
    stations = data
elif isinstance(data, dict):
    stations = data.get("stations", data.get("data"))

    if stations is None:
        raise ValueError(f"Unexpected API response: {list(data.keys())}")
else:
    raise ValueError("Unexpected response format")

df = pd.DataFrame(stations)

print("Total Delhi stations:", len(df))

columns = [
    "station_id",
    "station_name",
    "state_name",
    "city_name",
    "latitude",
    "longitude",
    "first_seen",
    "last_seen",
    "n_rows",
    "parameters"
]

available_columns = [col for col in columns if col in df.columns]

print(df[available_columns].to_string(index=False))

# Save station information
os.makedirs("data/raw", exist_ok=True)

df.to_csv("data/raw/delhi_stations.csv", index=False)

print("\nStation information saved successfully!")


# Display total station count
print("\nTotal Delhi stations:", len(df))

# Display station details
print("\nStation details:")

for _, row in df.iterrows():
    print(f"\nStation ID: {row.get('station_id')}")
    print(f"Station Name: {row.get('station_name')}")
    print(f"Parameters: {row.get('parameters')}")