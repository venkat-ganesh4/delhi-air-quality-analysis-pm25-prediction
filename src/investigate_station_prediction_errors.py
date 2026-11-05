import pandas as pd

input_file = "data/processed/delhi_2019_01_wide.csv"

df = pd.read_csv(input_file)

df["collected_at"] = pd.to_datetime(df["collected_at"])

# Stations with the largest prediction errors
stations = ["site_119", "site_1422"]

# Investigate January 28 to January 31
start_date = "2019-01-28"
end_date = "2019-02-01"

pollutants = [
    "PM2.5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "Ozone"
]

# Filter the observations
investigation = df[
    (df["station_id"].isin(stations)) &
    (df["collected_at"] >= start_date) &
    (df["collected_at"] < end_date)
]

investigation = investigation.sort_values(
    ["station_id", "collected_at"]
)

print("\nSTATION MEASUREMENT INVESTIGATION")

print(
    investigation[
        ["station_id", "station_name", "collected_at"] + pollutants
    ].to_string(index=False)
)