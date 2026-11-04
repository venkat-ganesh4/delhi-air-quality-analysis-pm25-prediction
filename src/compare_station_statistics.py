
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("XKDR_API_KEY")
BASE_URL = "https://airquality.xkdr.org/v1/measurements"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

station_groups = {
    "Lodhi Road": ["site_109", "site_5395"],
    "Pusa": ["site_107", "site_1563"]
}

def get_station_data(station_id):

    params = {
        "station": station_id,
        "parameter": "PM2.5",
        "start": "2024-11-01",
        "end": "2024-12-01",
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

    return df[["collected_at", "value"]].rename(
        columns={"value": station_id}
    )


for location, station_ids in station_groups.items():

    first_id, second_id = station_ids

    df1 = get_station_data(first_id)
    df2 = get_station_data(second_id)

    comparison = pd.merge(
        df1,
        df2,
        on="collected_at",
        how="inner"
    )

    print(f"\n{'=' * 45}")
    print(f"Location: {location}")
    print(f"{'=' * 45}")

    print(f"{first_id} readings: {len(df1)}")
    print(f"{second_id} readings: {len(df2)}")
    print(f"Matching timestamps: {len(comparison)}")

    print("\nStation statistics:")

    print(df1[first_id].describe())
    print(df2[second_id].describe())

    if not comparison.empty:

        comparison["absolute_difference"] = (
            comparison[first_id] - comparison[second_id]
        ).abs()

        print("\nComparison:")
        print(
            "Mean absolute difference:",
            round(comparison["absolute_difference"].mean(), 2)
        )

        print(
            "Correlation:",
            round(comparison[first_id].corr(comparison[second_id]), 4)
        )
