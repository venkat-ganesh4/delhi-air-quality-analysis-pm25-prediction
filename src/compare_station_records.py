
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("XKDR_API_KEY")
BASE_URL = "https://airquality.xkdr.org/v1/measurements"
station_groups = {
    "Lodhi Road": ["site_109", "site_5395"],
    "Pusa": ["site_107", "site_1563"]
}

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

station_data = {}

for station_name, station_ids in station_groups.items():

    for station_id in station_ids:

        params = {
            "station": station_id,
            "parameter": "PM2.5",
            "start": "2024-11-01",
            "end": "2024-11-07",
            "agg": "raw",
            "limit": 10000
        }

        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()["data"]

        df = pd.DataFrame(data)
        df["collected_at"] = pd.to_datetime(df["collected_at"])

        station_data[station_id] = df[
            ["collected_at", "value"]
        ].rename(columns={"value": station_id})

        print(f"{station_id}: {len(df)} readings")

    first_id, second_id = station_ids

    comparison = pd.merge(
        station_data[first_id],
        station_data[second_id],
        on="collected_at",
        how="inner"
    )

    print(f"\n--- {station_name} comparison ---")
    print("Matching timestamps:", len(comparison))

    if len(comparison) > 0:
        identical = (
            comparison[first_id] == comparison[second_id]
        ).sum()

        correlation = comparison[first_id].corr(
            comparison[second_id]
        )

        print("Identical readings:", identical)
        print("Different readings:", len(comparison) - identical)
        print("Correlation:", round(correlation, 4))

    print()
